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

    found, examples = set(), []
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
            examples.append(Example(
                conversation=cid, turn=i, case1=c1, case2=c2,
                user_text=turn.get("user_text", ""),
                ai_text=turn.get("ai_text", ""),
                strategy=(turn.get("strategy") or "").strip(),
            ))

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
