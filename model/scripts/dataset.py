#!/usr/bin/env python3
"""The one loader everybody trains and evaluates through.

Reads model/splits.json and hands back examples for a split. Import this rather
than globbing the JSON directory yourself - four loaders written separately will
disagree about which conversations are in which split, and the results table
stops meaning anything the moment they do.

    from dataset import load, Example

    train = load("train")           # list[Example]
    test  = load("test")

Each Example is one conversation turn and carries both training strings:

    case1  instruction + user text                        (no physiology)
    case2  instruction + user text + physiological summary

Arranging those into a training stream - interleaved, batched, randomised - is
the data-formatting experiment and belongs to that lane, not here. This module
deliberately returns them unordered-but-stable so the arrangement is visible in
the experiment's own code rather than hidden in the loader.

    python3 model/scripts/dataset.py        # summarise every split
"""

import json
import re
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
DATA = ROOT / "website" / "public" / "data" / "json"
SPLITS = ROOT / "model" / "splits.json"

FILENAME = re.compile(
    r"output_participantGrouped(?P<pid>.+?)data(?P<mod>_modified[a-zA-Z_]*)?_full_data\.json$")


def _demojibake(text):
    """Undo UTF-8 that was read as latin-1 somewhere upstream.

    271 of the 993 turns carry it, 974 occurrences, almost all in ai_text -
    "It\u2019s" arrives as "It\u00e2\u0080\u0099s". That is the completion, which is
    the span we compute loss on, so left alone the model learns to emit the
    broken bytes. Repaired here rather than in the JSON because this loader is
    the one thing every lane imports; the generator that wrote the files still
    needs the same fix, see model/TASKS.md.

    Only applied when the round trip is clean, so genuine accented characters
    (a participant writing "cafe\u0301") are never mangled by the repair itself.
    """
    if "\u00e2" not in text and "\u00c3" not in text and "\u00c2" not in text:
        return text
    try:
        return text.encode("latin-1").decode("utf-8")
    except (UnicodeEncodeError, UnicodeDecodeError):
        return text


@dataclass(frozen=True)
class Example:
    conversation: str          # "8", "8-modified", "11_1"
    turn: int                  # 1-based within the conversation
    case1: str                 # text only
    case2: str                 # text + physiological summary
    user_text: str
    ai_text: str               # the reference response
    strategy: str


def _conversation_id(path):
    m = FILENAME.match(path.name)
    if not m:
        return None
    return m.group("pid") + (m.group("mod") or "").replace("_", "-")


def load_splits():
    if not SPLITS.exists():
        raise SystemExit("model/splits.json is missing - run model/scripts/make_splits.py first")
    return json.loads(SPLITS.read_text())


def load(split):
    """Every turn of every conversation in `split`, in a stable order."""
    spec = load_splits()
    if split not in spec["splits"]:
        raise ValueError(f"unknown split {split!r}; expected one of {list(spec['splits'])}")
    wanted = set(spec["splits"][split]["conversations"])

    found, examples, unlabelled = set(), [], []
    for path in sorted(DATA.glob("output_participantGrouped*_full_data.json")):
        cid = _conversation_id(path)
        if cid not in wanted:
            continue
        found.add(cid)
        turns = [t for s in json.loads(path.read_text()) for t in s["turns"]]
        for i, turn in enumerate(turns, 1):
            c1 = turn.get("training_string_case1") or ""
            c2 = turn.get("training_string_case2") or ""
            if not c1 or not c2:
                # An incomplete pair would quietly unbalance the case1/case2
                # ratio, which is the very thing the formatting experiment
                # measures. Louder to stop than to skip.
                raise SystemExit(f"{cid} turn {i}: missing case1 or case2")
            if split == "train" and not (turn.get("strategy") or "").strip():
                # 67 of 687 training turns have no strategy, and their training
                # string literally reads "Strategy: \n\nResponse: ...". At 9.8%
                # of the data that was enough for the baseline to emit a blank
                # strategy on 138 of 155 test turns under greedy decoding - 89%,
                # from 10% of the data. A turn with no label cannot teach
                # strategy selection, and it actively teaches the model to skip
                # the field, so it is dropped from training.
                # Only from training: validation and test have no blanks at all,
                # so nothing is removed from anything that gets scored.
                unlabelled.append((cid, i))
                continue
            examples.append(Example(
                conversation=cid, turn=i,
                case1=_demojibake(c1), case2=_demojibake(c2),
                user_text=_demojibake(turn.get("user_text", "")),
                ai_text=_demojibake(turn.get("ai_text", "")),
                strategy=(turn.get("strategy") or "").strip(),
            ))

    if unlabelled:
        print(f"  dropped {len(unlabelled)} unlabelled training turns "
              f"(blank strategy teaches a blank Strategy line)")

    missing = wanted - found
    if missing:
        raise SystemExit(f"{split}: no file for {', '.join(sorted(missing))} - "
                         f"splits.json and the data directory disagree")
    return examples


def main():
    spec = load_splits()
    print(f"split file: seed {spec['seed']}, grouped by {spec['group_by']}")
    print(f"{spec['totals']['conversations']} conversations, "
          f"{spec['totals']['turns']} turns, "
          f"{spec['totals']['training_strings']} training strings\n")
    total = 0
    for name in ("train", "validation", "test"):
        ex = load(name)
        total += len(ex)
        chars = sum(len(e.case2) for e in ex) / max(len(ex), 1)
        print(f"  {name:<11} {len(ex):>4} turns -> {len(ex) * 2:>4} strings   "
              f"{len(set(e.conversation for e in ex)):>2} conversations   "
              f"mean case2 {chars:>5.0f} chars")
    print(f"\n  loaded {total} turns in total ({total * 2} strings)")

    broken = sum(1 for n in ("train", "validation", "test") for e in load(n)
                 if "\u00e2\u0080" in e.case2)
    print(f"  mojibake after repair: {broken} turns")

    # The guarantee the whole table rests on.
    seen = {}
    for name in ("train", "validation", "test"):
        for e in load(name):
            if e.conversation in seen and seen[e.conversation] != name:
                raise SystemExit(f"LEAK: {e.conversation} in both {seen[e.conversation]} "
                                 f"and {name}")
            seen[e.conversation] = name
    print("  no conversation appears in more than one split")


if __name__ == "__main__":
    main()
