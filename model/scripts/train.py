#!/usr/bin/env python3
"""Run one experiment from one config file.

    python3 model/scripts/train.py model/configs/baseline.json
    python3 model/scripts/train.py model/configs/baseline.json --smoke

Everything that distinguishes one row of model/RESULTS.md from another lives in
the config, not here: the model, the fine-tuning method, the data arrangement.
Change a config, give it a new run_id, and this script produces a checkpoint and
a run.json under model/runs/<run_id>/. Nobody should be editing this file to get
a different experiment - if an experiment cannot be expressed as a config, say
so on the group rather than forking the script.

--smoke tokenises everything, prints the label masking for one example, and
exits before any weights load. It needs no GPU and about 20 seconds, and it is
the only way to catch a masking or truncation bug without burning server hours.
"""

import argparse
import json
import random
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from dataset import load  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent.parent
RUNS = ROOT / "model" / "runs"

RESPONSE_MARKER = "### Response:"
EOS_LITERAL = "<EOS>"


def build_stream(examples, arrangement, seed):
    """Order the case1/case2 strings into the sequence the model sees.

    This ordering IS Siddaarth's experiment, which is why the sampler below is
    sequential - see the note on NoShuffleTrainer. Returns (text, case) pairs so
    the run manifest can prove the arrangement came out the way it was asked for.
    """
    if arrangement == "interleaved":
        stream = [p for e in examples for p in ((e.case1, 1), (e.case2, 2))]
    elif arrangement == "batched":
        # All 993 case1 strings, then all 993 case2. Whether "batched" was meant
        # globally or per optimiser batch is genuinely ambiguous in the brief;
        # global is the reading that actually contrasts with interleaved.
        stream = [(e.case1, 1) for e in examples] + [(e.case2, 2) for e in examples]
    elif arrangement == "randomised":
        stream = [p for e in examples for p in ((e.case1, 1), (e.case2, 2))]
        random.Random(seed).shuffle(stream)
    else:
        raise SystemExit(f"unknown data.format {arrangement!r}: "
                         "expected interleaved, batched or randomised")
    return stream


def encode(text, tokenizer, max_len, loss_on):
    """One training string -> input_ids + labels, prompt masked to -100.

    Split on the literal marker and tokenise the two halves separately rather
    than using offset mapping: it works on slow tokenisers too, and a wrong
    boundary here silently trains on the wrong span instead of erroring.
    """
    head, sep, tail = text.partition(RESPONSE_MARKER)
    if not sep:
        raise ValueError("no '### Response:' marker")

    prompt = head + RESPONSE_MARKER
    completion = tail.replace(EOS_LITERAL, "")

    prompt_ids = tokenizer(prompt, add_special_tokens=True)["input_ids"]
    completion_ids = tokenizer(completion, add_special_tokens=False)["input_ids"]
    completion_ids.append(tokenizer.eos_token_id)

    if loss_on == "completion_only":
        labels = [-100] * len(prompt_ids) + list(completion_ids)
    else:
        labels = list(prompt_ids) + list(completion_ids)

    ids = prompt_ids + completion_ids
    truncated = len(ids) > max_len
    if truncated:
        # Cutting from the right removes the completion, which leaves an example
        # whose labels are entirely -100: it contributes no gradient and quietly
        # shrinks the effective dataset. Drop the middle of the prompt instead,
        # which for case2 is the physiological narration, and keep both the
        # instruction header and the whole response.
        keep_completion = len(completion_ids)
        room = max_len - keep_completion
        if room < 64:
            return None, None, True
        head_keep = room // 2
        prompt_ids = prompt_ids[:head_keep] + prompt_ids[-(room - head_keep):]
        ids = prompt_ids + completion_ids
        labels = ([-100] * len(prompt_ids) + list(completion_ids)
                  if loss_on == "completion_only" else list(ids))

    return ids, labels, truncated


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("config", type=Path)
    ap.add_argument("--smoke", action="store_true",
                    help="tokenise and report, load no weights, train nothing")
    ap.add_argument("--split", default="train")
    args = ap.parse_args()

    cfg = json.loads(args.config.read_text())
    run_id = cfg["run_id"]
    seed = cfg["seed"]
    data_cfg, ft = cfg["data"], cfg["finetune"]
    loss_on = data_cfg.get("loss_on", "completion_only")

    from transformers import AutoTokenizer

    tokenizer = AutoTokenizer.from_pretrained(cfg["model"]["name"])
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token

    examples = load(args.split)
    stream = build_stream(examples, data_cfg["format"], seed)
    max_len = cfg["model"]["max_seq_len"]

    rows, dropped, truncated, unmasked = [], 0, 0, 0
    for text, case in stream:
        ids, labels, was_cut = encode(text, tokenizer, max_len, loss_on)
        if ids is None:
            dropped += 1
            continue
        truncated += was_cut
        if all(l == -100 for l in labels):
            unmasked += 1
            continue
        rows.append({"input_ids": ids, "labels": labels, "case": case})

    print(f"run {run_id}: {len(rows)} training strings from {len(examples)} turns "
          f"({data_cfg['format']}, loss on {loss_on})")
    lens = sorted(len(r["input_ids"]) for r in rows)
    print(f"  length: median {lens[len(lens) // 2]}, p95 {lens[int(len(lens) * .95)]}, "
          f"max {lens[-1]} of {max_len}")
    supervised = sum(sum(1 for l in r["labels"] if l != -100) for r in rows)
    print(f"  supervised tokens: {supervised} of {sum(lens)} "
          f"({100 * supervised / sum(lens):.0f}%)")
    if truncated:
        print(f"  truncated: {truncated} (prompt middle removed, response kept)")
    if dropped or unmasked:
        print(f"  DROPPED {dropped + unmasked} - response longer than the window")

    if args.smoke:
        r = rows[0]
        cut = next(i for i, l in enumerate(r["labels"]) if l != -100)
        print("\n  masked tail  ..." + tokenizer.decode(r["input_ids"][cut - 12:cut]))
        print("  learned head " + tokenizer.decode(r["input_ids"][cut:cut + 24]) + "...")
        print("\n  smoke only, nothing trained")
        return

    import torch
    from transformers import (AutoModelForCausalLM, Trainer, TrainingArguments,
                              DataCollatorForSeq2Seq)
    from torch.utils.data import SequentialSampler

    bf16 = torch.cuda.is_available() and torch.cuda.is_bf16_supported()
    if torch.cuda.is_available():
        print(f"  {torch.cuda.get_device_name(0)}, "
              f"{'bf16' if bf16 else 'fp16 (no bf16 on this card)'}")

    class NoShuffleTrainer(Trainer):
        # The whole point of the formatting lane is the ORDER of the examples.
        # Trainer shuffles the train dataloader by default, which would collapse
        # interleaved, batched and randomised into the same experiment and make
        # three rows of the results table identical for no visible reason.
        def _get_train_sampler(self, *a, **kw):
            return SequentialSampler(self.train_dataset)

    out = RUNS / run_id
    out.mkdir(parents=True, exist_ok=True)

    model = AutoModelForCausalLM.from_pretrained(
        cfg["model"]["name"],
        dtype=torch.bfloat16 if bf16 else torch.float16,
    )
    if ft.get("gradient_checkpointing"):
        model.gradient_checkpointing_enable()
        model.config.use_cache = False

    val = [dict(zip(("input_ids", "labels"),
                    encode(e.case2, tokenizer, max_len, loss_on)[:2]))
           for e in load("validation")]

    trainer = NoShuffleTrainer(
        model=model,
        train_dataset=[{k: r[k] for k in ("input_ids", "labels")} for r in rows],
        eval_dataset=[v for v in val if v["input_ids"]],
        data_collator=DataCollatorForSeq2Seq(tokenizer, padding=True, label_pad_token_id=-100),
        args=TrainingArguments(
            output_dir=str(out),
            seed=seed,
            num_train_epochs=ft["epochs"],
            learning_rate=ft["learning_rate"],
            lr_scheduler_type=ft["lr_scheduler"],
            warmup_ratio=ft["warmup_ratio"],
            weight_decay=ft["weight_decay"],
            per_device_train_batch_size=ft["per_device_batch_size"],
            gradient_accumulation_steps=ft["gradient_accumulation_steps"],
            gradient_checkpointing=ft.get("gradient_checkpointing", False),
            optim=ft.get("optimizer", "adamw_torch"),
            bf16=bf16,
            fp16=not bf16 and torch.cuda.is_available(),
            group_by_length=False,   # would reorder the stream, same trap as shuffling
            logging_steps=10,
            eval_strategy="epoch",
            save_strategy="epoch",
            save_total_limit=2,
            report_to=[],
        ),
    )
    result = trainer.train()
    trainer.save_model(str(out / "final"))
    tokenizer.save_pretrained(str(out / "final"))

    history = [h for h in trainer.state.log_history if "eval_loss" in h]
    (out / "run.json").write_text(json.dumps({
        "run_id": run_id,
        "config": str(args.config.relative_to(ROOT)),
        "arrangement": data_cfg["format"],
        "loss_on": loss_on,
        "training_strings": len(rows),
        "dropped": dropped + unmasked,
        "precision": "bf16" if bf16 else "fp16",
        "train_loss": result.training_loss,
        "eval_loss_per_epoch": [h["eval_loss"] for h in history],
    }, indent=2) + "\n")
    print(f"\n  wrote {out}/run.json - copy the numbers into model/RESULTS.md")


if __name__ == "__main__":
    main()
