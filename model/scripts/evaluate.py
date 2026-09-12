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
    physio_grounding        physio_grounded_clean: qualitative reference to the
                            body with no leaked number/unit/channel name, per
                            the rule in evaluation/scripts/render.py, alongside
                            physio_leak_rate and physio_mention_rate_naive (the
                            old metric, kept only for comparison - it scored a
                            response that reads raw values back at the user as
                            "grounded", backwards from the rule). Also: did the
                            physiological summary change the answer
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
#
# Kept for backward comparison only (physio_mention_rate_naive below). This is
# the metric the brief flagged as wrong: it mixes qualitative body words
# ("restless", "body") with the raw jargon those words exist to avoid ("bpm",
# "degc", "electrodermal", "eda"), so a response that just reads the channel
# values back at the user scores exactly as "grounded" as one that reflects
# them qualitatively - the opposite of what grounding is supposed to reward.
SIGNAL_TERMS = ("heart rate", "bpm", "temperature", "degc", "electrodermal",
                "eda", "skin conductance", "movement", "activity", "stress",
                "arousal", "breathing", "physical", "body", "restless", "still")

# The actual rule, from evaluation/scripts/render.py: the physiological summary
# is hidden from the user, and every worked example in the master prompt refers
# to it qualitatively ("gentle cues", "your physical response seems fairly
# even"). A response may reflect the physiological state but must never quote a
# number, a unit, or a channel name back at them. render.py enforces this on
# the hand-authored responses via LEAK_RE/BODY_RE/leaks() - duplicated here
# rather than imported, since render.py pulls in python-docx for report
# generation this scorer has no other reason to depend on. If the rule in
# render.py changes, change it here too.
LEAK_RE = re.compile(
    r"\bEDA\b|\bPR\b|\bACCEL\b|\bbpm\b|\buS\b|\bdegC\b|conductance|microsiemens"
    r"|accelerometer|electrodermal|skin temperature|activity count|stress score"
)
BODY_RE = re.compile(
    r"\bpulse\b|heart rate|\barousal\b|\bsignals?\b|\breadings?\b|\bphysical\b|\bbody\b"
    r"|\bmovement\b|\btension\b|\bbreathing\b", re.I)


def physio_leaks(response):
    """Channel jargon anywhere, or a figure quoted next to a body reference.

    Mirrors render.py's leaks(): a number is only a leak when it sits beside a
    reference to the body, so a CGPA or an OWASP list number the user quoted
    stays clean while "your pulse dropped to 90" does not. Checked per sentence
    so the two never get confused.
    """
    found = list(LEAK_RE.findall(response))
    for sentence in re.split(r"(?<=[.!?])\s+|\s-\s", response):
        if BODY_RE.search(sentence):
            found += re.findall(r"\d+(?:\.\d+)?", sentence)
    return found


def physio_qualitative_mention(response):
    """A soft, non-jargon reference to bodily/physiological state."""
    return bool(BODY_RE.search(response))

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


def canon_vocab(k=12):
    """The k most common normalised strategies across the whole corpus.

    Scored F1 sits at 0.13-0.16 against 132 labels, 48 of which appear once. That
    is mostly a label problem: a model answering "Emotional Validation" where the
    reference says "Empathic Reflection" is not obviously wrong, and there is not
    enough data to separate those classes anyway. Collapsing the tail into
    "other" and scoring again says how much of the error is real disagreement
    rather than an over-specified label set.

    Scoring only. Consolidating the labels in the training strings would
    invalidate every row in the table and is a decision for the group.
    """
    from collections import Counter
    seen = Counter()
    for split in ("train", "validation", "test"):
        for e in load(split):
            for part in strategy_set(e.strategy):
                seen[part] += 1
    return {lbl for lbl, _ in seen.most_common(k)}


def consolidate(labels, vocab):
    return {l if l in vocab else "other" for l in labels} or {"other"}


def f1(ref, got):
    if not ref and not got:
        return None
    inter = len(ref & got)
    p = inter / len(got) if got else 0.0
    r = inter / len(ref) if ref else 0.0
    return 0.0 if p + r == 0 else 2 * p * r / (p + r)


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
    # Reusing the cache is only safe while the weights that produced it are the
    # weights being scored. A retrained run leaves a newer checkpoint beside an
    # older generations.jsonl, and reusing it would score the previous model and
    # report the numbers under the new run's name - a confidently wrong result
    # with nothing visibly broken.
    weights = max((f.stat().st_mtime for f in ckpt.glob("*.safetensors")), default=0)
    stale = cache.exists() and cache.stat().st_mtime < weights
    if stale:
        print(f"  {cache.name} predates the checkpoint - regenerating")
    if cache.exists() and not stale and not args.regenerate:
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
    vocab = canon_vocab()
    # The number every strategy score has to be read against. Always answering
    # the single most common label scores 0.16 on this test split, so a model at
    # 0.16 has learned nothing about strategy selection. Reporting strategy F1
    # without this alongside it invites the table to claim a capability that is
    # not there.
    majority = {"emotionalvalidation"}
    strat_f1, top_f1, base_f1 = [], [], []
    fmt_ok, reps, truncs, spec, echoes, diverged = 0, [], 0, [], [], 0
    grounded_naive, grounded_qual, leaked = 0, 0, 0
    for key, cases in by_turn.items():
        if 2 not in cases:
            continue
        strat2, resp2, raw2, ex = cases[2]
        ref = strategy_set(ex.strategy)
        got = strategy_set(strat2)
        if ref or got:
            strat_f1.append(f1(ref, got))
            top_f1.append(f1(consolidate(ref, vocab), consolidate(got, vocab)))
            base_f1.append(f1(ref, majority))
        fmt_ok += bool(strat2 and resp2)
        reps.append(repetition(resp2))
        truncs += not raw2.rstrip().endswith((".", "!", "?", '"'))
        s, ec = specificity(resp2, ex.user_text)
        spec.append(s)
        echoes.append(ec)
        # Old metric, kept only so the tightened one below can be defended
        # against it: any signal term at all, jargon included.
        grounded_naive += any(t in resp2.lower() for t in SIGNAL_TERMS)
        # Tightened metric: qualitative reference to the body, with no leaked
        # jargon or raw value. This is the one that enforces the render.py
        # rule - a response that quotes a number or a channel name back at the
        # user does not score as grounded no matter how directly it engages
        # with the physiological state.
        this_leaks = bool(physio_leaks(resp2))
        leaked += this_leaks
        grounded_qual += physio_qualitative_mention(resp2) and not this_leaks
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
            "strategy_f1_top12": round(sum(top_f1) / max(len(top_f1), 1), 4),
            "strategy_f1_majority_baseline": round(sum(base_f1) / max(len(base_f1), 1), 4),
            "format_compliance": round(fmt_ok / n, 4),
            "physio_grounded_clean": round(grounded_qual / n, 4),
            "physio_leak_rate": round(leaked / n, 4),
            "physio_mention_rate_naive": round(grounded_naive / n, 4),
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
