#!/usr/bin/env python3
"""Run a trained model over hand-written cases and write one CSV row per prompt.

    python3 model/scripts/generate_cases.py model/runs/smollm2-1.7b-1gpu-lr2e5 \\
        model/eval_cases/stage2_cases.json

A cases file is a list of groups: one user text, several physiological variants
(for the supplied scenarios: mild, severe, and none). Every variant of a group
gets its own row, so the CSV answers the question the cases were written for -
does the answer move when only the physiology moves.

This is not the harness. evaluate.py scores the frozen test split; this runs
text nobody trained or validated on, including our own conversations, and
scores nothing. Greedy for the same reason as evaluate.py: a CSV that changes
every time it is regenerated cannot be quoted.
"""

import argparse
import csv
import json
import sys
from itertools import combinations
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from dataset import load  # noqa: E402
from evaluate import RESPONSE_MARKER, parse, strategy_set  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent.parent
OUT = ROOT / "model" / "eval_cases" / "out"


def physio_field(physio):
    """The supplied summary, laid out the way training strings carry it.

    Training puts the summary on a single line and writes the absent case as
    "Not Available" with no full stop. The supplied cases break lines and write
    "Not Available.". Same words either way, but left as supplied, the no-physio
    row would be testing punctuation the model never saw rather than absence.
    """
    flat = " ".join(physio.split())
    return "Not Available" if flat.rstrip(".") == "Not Available" else flat


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("run_dir", type=Path, help="model/runs/<run_id>")
    ap.add_argument("cases", type=Path, help="model/eval_cases/<name>.json")
    ap.add_argument("--batch", type=int, default=8)
    args = ap.parse_args()

    ckpt = args.run_dir / "final"
    if not ckpt.exists():
        raise SystemExit(f"{ckpt} does not exist - has this run finished?")

    # Taken from the data rather than retyped: all 993 turns carry one identical
    # 417-character header, and a single changed character here would put every
    # prompt slightly outside what the model was trained on.
    header = load("test")[0].case1.partition("### Input:")[0]

    groups = json.loads(args.cases.read_text())["scenarios"]
    rows, prompts = [], []
    for g in groups:
        for v in g["variants"]:
            physio = physio_field(v["physio"])
            prompts.append(f"{header}### Input:\nText: {g['text']}\n"
                           f"Physiological Signals: {physio}\n\n{RESPONSE_MARKER}")
            rows.append({"scenario": g["scenario"], "group": g["group"],
                         "text": g["text"], "label": v["label"], "physio": physio})

    import torch
    from transformers import AutoModelForCausalLM, AutoTokenizer

    tok = AutoTokenizer.from_pretrained(ckpt)
    tok.padding_side = "left"
    if tok.pad_token is None:
        tok.pad_token = tok.eos_token
    model = AutoModelForCausalLM.from_pretrained(
        ckpt, dtype=torch.float16 if torch.cuda.is_available() else torch.float32)
    model.eval()
    if torch.cuda.is_available():
        model.cuda()

    print(f"{args.run_dir.name}: {len(prompts)} prompts from {len(groups)} groups "
          f"in {args.cases.name}")
    for i in range(0, len(prompts), args.batch):
        enc = tok(prompts[i:i + args.batch], return_tensors="pt", padding=True)
        enc = {k: v.to(model.device) for k, v in enc.items()}
        with torch.no_grad():
            out = model.generate(**enc, max_new_tokens=300, do_sample=False,
                                 num_beams=1, pad_token_id=tok.pad_token_id)
        for j, (seq, src) in enumerate(zip(out, enc["input_ids"])):
            raw = tok.decode(seq[len(src):], skip_special_tokens=True)
            strategy, response = parse(raw)
            rows[i + j].update(strategy=strategy or "(none)",
                               response=response or raw.strip())

    OUT.mkdir(parents=True, exist_ok=True)
    dest = OUT / f"{args.cases.stem}__{args.run_dir.name}.csv"
    with dest.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["scenario", "group", "text", "label",
                                          "physio", "strategy", "response"])
        w.writeheader()
        w.writerows(rows)

    compare(rows)
    print(f"  wrote {dest.relative_to(ROOT)}")


def compare(rows):
    """Per pair of variants, how many groups got a different answer.

    Lumping the variants together hides the one distinction these cases exist
    for: an answer that moves when a summary appears but not when it goes from
    mild to severe is reacting to the summary being there, not to what it says.
    Strategies are compared normalised, or "EmotionalValidation" against
    "Emotional Validation" counts as the model changing its mind.
    """
    by_group = {}
    for r in rows:
        by_group.setdefault(r["group"], {})[r["label"]] = r
    labels = []
    for variants in by_group.values():
        labels += [l for l in variants if l not in labels]
    for a, b in combinations(labels, 2):
        pairs = [(v[a], v[b]) for v in by_group.values() if a in v and b in v]
        resp = sum(x["response"] != y["response"] for x, y in pairs)
        strat = sum(strategy_set(x["strategy"]) != strategy_set(y["strategy"])
                    for x, y in pairs)
        print(f"  {a} vs {b}: response differs in {resp}/{len(pairs)}, "
              f"strategy in {strat}/{len(pairs)}")


if __name__ == "__main__":
    main()
