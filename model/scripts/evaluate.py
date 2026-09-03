#!/usr/bin/env python3
"""Score one trained run on the frozen test split.

    python3 model/scripts/evaluate.py model/runs/baseline
    python3 model/scripts/evaluate.py model/runs/baseline --limit 20

Writes scores.json and generations.jsonl next to the checkpoint. Every model in
model/RESULTS.md must be scored through this file, on the test conversations in
model/splits.json, or the rows are not comparable.

Generation is greedy - do not add sampling. Two evaluations of one checkpoint
have to produce identical scores, otherwise a difference between two rows of the
table might be sampling noise rather than a difference between the models.

WHAT THIS MEASURES, AND WHAT IT DOES NOT

Four of the six parameters in the brief can be computed from the generations
without a judge, and are:

    strategy_faithfulness   did the model pick the reference strategy
    physio_grounding        did the physiological summary change the answer
    specificity             concrete content rather than generic comfort
    fluency                 no loops, no truncation mid-sentence

Two cannot be, and this file does not pretend otherwise:

    empathy                 needs a person or a judge model
    safety                  needs a person or a judge model

They come out null. generations.jsonl is written in a shape that a human or a
judge model can score directly, and scores.json has slots waiting for those
numbers. A scripted proxy for empathy - counting warm-sounding words - would
produce a number that looks like a result and means nothing, and the table is
easier to defend with an honest gap in it than with a fabricated column.
"""

import argparse
import json
import re
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from dataset import load  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent.parent
RESPONSE_MARKER = "### Response:"

# The physiological narration is built from these signals, so a response that
# grounds itself in the body has to touch at least one of them. Checked against
# the response text only, never against the prompt it was copied from.
SIGNAL_TERMS = ("heart rate", "bpm", "temperature", "degc", "electrodermal",
                "eda", "skin conductance", "movement", "activity", "stress",
                "arousal", "breathing", "physical", "body", "restless", "still")

# Words that carry no information about this particular person's situation. A
# response made only of these is fluent, kind, and useless, which is exactly the
# failure mode specificity is meant to catch.
GENERIC = frozenset("""a an the and or but so if it its is are was were be been being to of
in on at for with from that this these those you your yours i me my we our they them he she
it's you're i'm can could would should will may might do does did have has had feel feels
feeling felt just really very much more most some any all thing things way ways okay ok
sure yes no not never always sometimes often about like as by than then there here what
when where who how why okay sure""".split())

# \s* after the colon would cross a newline, so a model that emits a bare
# "Strategy:" followed by its response on the next line had the whole response
# captured as its strategy - scoring it wrong AND reporting perfect format
# compliance. The strategy is one line; only the response may span lines.
STRATEGY_LINE = re.compile(r"strategy[ \t]*:[ \t]*([^\n]*)", re.I)
RESPONSE_LINE = re.compile(r"response[ \t]*:[ \t]*(.+)", re.I | re.S)


def norm_label(s):
    """'Emotional Validation' and 'EmotionalValidation' are the same strategy.

    206 raw surface forms collapse to 132 once case and spacing go, and seven of
    those collisions cover 336 turns. Comparing raw strings would mark a model
    wrong for whitespace on a third of the corpus.
    """
    return re.sub(r"[^a-z]", "", s.lower())


def strategy_set(text):
    """Strategies as a set - 173 turns carry two, so this is multi-label."""
    return {norm_label(p) for p in text.split(",") if norm_label(p)}


def parse(generated):
    """Pull the Strategy and Response back out of what the model emitted."""
    strat = STRATEGY_LINE.search(generated)
    resp = RESPONSE_LINE.search(generated)
    return (strat.group(1).strip() if strat else "",
            resp.group(1).strip() if resp else "")


def repetition(text, n=4):
    """Share of n-grams that are repeats. Small models loop when overtrained."""
    words = text.lower().split()
    if len(words) <= n:
        return 0.0
    grams = [tuple(words[i:i + n]) for i in range(len(words) - n + 1)]
    return 1 - len(set(grams)) / len(grams)


def specificity(response, user_text):
    """Content words that are not filler, and how many echo the user's own situation.

    Two components because they fail differently: a response can be full of
    concrete nouns that have nothing to do with what the person said, or it can
    parrot the user's words back with no substance of its own.
    """
    words = [w for w in re.findall(r"[a-z']+", response.lower())]
    if not words:
        return 0.0, 0.0
    content = [w for w in words if w not in GENERIC and len(w) > 3]
    user_words = {w for w in re.findall(r"[a-z']+", user_text.lower())
                  if w not in GENERIC and len(w) > 3}
    echo = sum(1 for w in content if w in user_words)
    return len(set(content)) / len(words), echo / max(len(content), 1)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("run_dir", type=Path, help="model/runs/<run_id>")
    ap.add_argument("--limit", type=int, help="score only the first N turns")
    ap.add_argument("--batch", type=int, default=8)
    ap.add_argument("--regenerate", action="store_true",
                    help="ignore an existing generations.jsonl and generate again")
    args = ap.parse_args()

    ckpt = args.run_dir / "final"
    if not ckpt.exists():
        raise SystemExit(f"{ckpt} does not exist - has this run finished?")

    turns = load("test")
    if args.limit:
        turns = turns[:args.limit]

    # Generation is the expensive half and the scoring is the half that changes,
    # so a finished generations.jsonl is reused rather than recomputed. A bug in
    # a metric should cost seconds, not another pass over 310 prompts on a GPU.
    cache = args.run_dir / "generations.jsonl"
    if cache.exists() and not args.regenerate:
        records = [json.loads(l) for l in cache.read_text().splitlines() if l.strip()]
        if len(records) == len(turns) * 2:
            print(f"scoring {args.run_dir.name} from {cache.name} "
                  f"({len(records)} cached generations, --regenerate to redo)")
            return score(args.run_dir, ckpt, turns, records)
        print(f"  {cache.name} has {len(records)} rows, expected {len(turns) * 2} "
              f"- regenerating")

    import torch
    from transformers import AutoModelForCausalLM, AutoTokenizer

    tok = AutoTokenizer.from_pretrained(ckpt)
    # Decoder-only generation pads on the left, or the model continues from pad
    # tokens and the first real token of a short prompt lands in the wrong place.
    tok.padding_side = "left"
    if tok.pad_token is None:
        tok.pad_token = tok.eos_token

    model = AutoModelForCausalLM.from_pretrained(
        ckpt, dtype=torch.float16 if torch.cuda.is_available() else torch.float32)
    model.eval()
    if torch.cuda.is_available():
        model.cuda()

    print(f"scoring {args.run_dir.name} on {len(turns)} test turns "
          f"({len(turns) * 2} generations, both cases)")

    prompts, meta = [], []
    for e in turns:
        for case, text in ((1, e.case1), (2, e.case2)):
            head, sep, _ = text.partition(RESPONSE_MARKER)
            prompts.append(head + RESPONSE_MARKER)
            meta.append((e, case))

    outputs = []
    for i in range(0, len(prompts), args.batch):
        chunk = prompts[i:i + args.batch]
        enc = tok(chunk, return_tensors="pt", padding=True, truncation=True,
                  max_length=2048)
        enc = {k: v.to(model.device) for k, v in enc.items()}
        with torch.no_grad():
            out = model.generate(**enc, max_new_tokens=300, do_sample=False,
                                 num_beams=1, pad_token_id=tok.pad_token_id)
        for row, src in zip(out, enc["input_ids"]):
            outputs.append(tok.decode(row[len(src):], skip_special_tokens=True))
        print(f"  {min(i + args.batch, len(prompts))}/{len(prompts)}", end="\r")
    print()

    records = []
    for (e, case), gen in zip(meta, outputs):
        strat, resp = parse(gen)
        records.append({"conversation": e.conversation, "turn": e.turn, "case": case,
                        "reference_strategy": e.strategy, "predicted_strategy": strat,
                        "reference_response": e.ai_text, "generated_response": resp,
                        "raw": gen})
    cache.write_text("".join(json.dumps(r) + "\n" for r in records))
    return score(args.run_dir, ckpt, turns, records)


def score(run_dir, ckpt, turns, records):
    """Metrics from generations, so a metric bug costs no GPU time to fix."""
    index = {(e.conversation, e.turn): e for e in turns}
    by_turn = {}
    for r in records:
        key = (r["conversation"], r["turn"])
        by_turn.setdefault(key, {})[r["case"]] = (
            r["predicted_strategy"], r["generated_response"], r["raw"], index[key])

    # --- metrics, case2 unless stated: that is the condition the project is about
    strat_f1, fmt_ok, reps, truncs, spec, echoes, grounded, diverged = [], 0, [], 0, [], [], 0, 0
    for key, cases in by_turn.items():
        if 2 not in cases:
            continue
        strat2, resp2, raw2, ex = cases[2]
        ref = strategy_set(ex.strategy)
        got = strategy_set(strat2)
        if ref or got:
            inter = len(ref & got)
            p = inter / len(got) if got else 0.0
            r = inter / len(ref) if ref else 0.0
            strat_f1.append(0.0 if p + r == 0 else 2 * p * r / (p + r))
        fmt_ok += bool(strat2 and resp2)
        reps.append(repetition(resp2))
        truncs += not raw2.rstrip().endswith((".", "!", "?", '"'))
        s, ec = specificity(resp2, ex.user_text)
        spec.append(s)
        echoes.append(ec)
        grounded += any(t in resp2.lower() for t in SIGNAL_TERMS)
        if 1 in cases:
            # If the physiological summary changes nothing, the model is ignoring
            # it - which is the single most important thing to know about a
            # project whose premise is that the signal helps.
            diverged += cases[1][1].strip() != resp2.strip()

    n = max(len(reps), 1)
    scores = {
        "run_id": run_dir.name,
        "checkpoint": str(ckpt.resolve().relative_to(ROOT)),
        "test_turns": len(turns),
        "generation": {"temperature": 0.0, "greedy": True, "max_new_tokens": 300},
        "computed": {
            "strategy_f1": round(sum(strat_f1) / max(len(strat_f1), 1), 4),
            "format_compliance": round(fmt_ok / n, 4),
            "physio_mention_rate": round(grounded / n, 4),
            "physio_changed_answer": round(diverged / n, 4),
            "specificity_content_ratio": round(sum(spec) / n, 4),
            "specificity_user_echo": round(sum(echoes) / n, 4),
            "repetition_4gram": round(sum(reps) / n, 4),
            "truncation_rate": round(truncs / n, 4),
        },
        "needs_a_judge": {
            "empathy": None,
            "safety": None,
            "how": "score generations.jsonl by hand or with a judge model, 1-5, "
                   "then fill these in. Do not compute them from word lists.",
        },
    }
    (run_dir / "scores.json").write_text(json.dumps(scores, indent=2) + "\n")

    print(f"\n  {run_dir.name}")
    for k, v in scores["computed"].items():
        print(f"    {k:<28} {v}")
    print(f"\n  wrote {run_dir}/scores.json and generations.jsonl")
    print("  empathy and safety are null until a person or a judge scores "
          "generations.jsonl")


if __name__ == "__main__":
    main()
