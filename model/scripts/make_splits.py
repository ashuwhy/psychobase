#!/usr/bin/env python3
"""Freeze the train / validation / test split, once, for everyone.

Run this once and commit model/splits.json. Every experiment loads that file.
If we each split separately, the numbers in the results table are not
comparable, and if the split moves between runs the table silently compares
models that were measured on different data.

Three leakage traps this avoids, in order of how much damage they do:

1. **Splitting inside a conversation.** Turns in one conversation share a
   participant, a scenario and a physiological session. Put turn 3 in training
   and turn 9 in test and the model has already seen the situation it is being
   tested on. Whole conversations move together.

2. **Separating a conversation from its modified rewrite.** "8" and
   "8-modified" are the same session with the dialogue rewritten - identical
   timestamps, identical physiological recording. Training on one and testing on
   the other tests memorisation of a physiological trace, not generalisation.
   Variants stay together.

3. **Separating sessions of the same participant.** 11, 11_1, 11_2 and 11_3 are
   the same person across four sessions about the same situation. Different
   conversations, but the same voice and the same story. Grouping them is the
   conservative choice and is the default here; --group-by file is available if
   we decide the finer split is worth the risk, since 25 groups is coarse.

Note that person_id in the source JSON is 2753 for 43 of 55 files, so it is a
device or batch identifier rather than a person. It cannot be used for grouping.

    python3 model/scripts/make_splits.py            # writes model/splits.json
    python3 model/scripts/make_splits.py --show     # print without writing
"""

import argparse
import json
import os
import re
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
DATA = ROOT / "website" / "public" / "data" / "json"
OUT = ROOT / "model" / "splits.json"

FILENAME = re.compile(
    r"output_participantGrouped(?P<pid>.+?)data(?P<mod>_modified[a-zA-Z_]*)?_full_data\.json$")

# Proportions are of *turns*, not of conversations - conversations run from 6 to
# 50 turns, so balancing by count would give wildly uneven splits.
TARGET = {"train": 0.70, "validation": 0.15, "test": 0.15}
SEED = 20260828


def conversations():
    """Every conversation file with its id, group, and turn count."""
    found = []
    for path in sorted(DATA.glob("output_participantGrouped*_full_data.json")):
        m = FILENAME.match(path.name)
        if not m:
            continue
        suffix = m.group("mod") or ""
        pid, modified = m.group("pid"), bool(suffix)
        turns = [t for s in json.loads(path.read_text()) for t in s["turns"]]
        # Every turn must carry both training strings or the pair is incomplete.
        complete = sum(1 for t in turns
                       if t.get("training_string_case1") and t.get("training_string_case2"))
        found.append({
            # Carry the whole suffix: participant 1 ships two modified
            # generations (_modified and _modified_phyS), and collapsing both to
            # "1-modified" gives two different files the same id, so a loader
            # keyed by id silently drops one.
            "id": pid + suffix.replace("_", "-"),
            "file": path.name,
            # 11_1 and 11_3 are sessions of participant 11; "8-modified" is a
            # rewrite of 8. Both collapse to the same group.
            "group": pid.split("_")[0],
            "modified": modified,
            "turns": len(turns),
            "complete_pairs": complete,
        })
    return found


def assign(groups, seed=SEED):
    """Greedy: hand the largest remaining group to whichever split is furthest
    below its target share of turns. Deterministic given the same input, and
    stable when a new conversation is added - unlike a shuffle, where one extra
    file reshuffles everything and invalidates every previous run."""
    total = sum(g["turns"] for g in groups)
    quota = {k: v * total for k, v in TARGET.items()}
    filled = {k: 0 for k in TARGET}
    out = {k: [] for k in TARGET}

    # Largest first, tie-broken by group name so the result never depends on
    # filesystem ordering.
    for group in sorted(groups, key=lambda g: (-g["turns"], g["name"])):
        split = max(filled, key=lambda k: (quota[k] - filled[k]) / quota[k] if quota[k] else 0)
        out[split].append(group)
        filled[split] += group["turns"]
    return out, filled, total


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--group-by", choices=["participant", "file"], default="participant",
                    help="participant (default) keeps 11, 11_1, 11_2, 11_3 together; "
                         "file treats each conversation as its own group")
    ap.add_argument("--show", action="store_true", help="print without writing")
    args = ap.parse_args()

    convs = conversations()
    key = "group" if args.group_by == "participant" else "id"
    # A "-modified" rewrite always travels with its original, whichever mode.
    if args.group_by == "file":
        for c in convs:
            c["id_group"] = c["id"].split("-modified")[0]
        key = "id_group"

    grouped = defaultdict(list)
    for c in convs:
        grouped[c[key]].append(c)
    groups = [{"name": name, "turns": sum(c["turns"] for c in members),
               "conversations": sorted(c["id"] for c in members)}
              for name, members in grouped.items()]

    splits, filled, total = assign(groups)

    payload = {
        "seed": SEED,
        "group_by": args.group_by,
        "generated_from": str(DATA.relative_to(ROOT)),
        "totals": {"conversations": len(convs), "groups": len(groups), "turns": total,
                   "training_strings": total * 2},
        "splits": {
            name: {
                "turns": filled[name],
                "share": round(filled[name] / total, 4),
                "groups": sorted(g["name"] for g in members),
                "conversations": sorted(c for g in members for c in g["conversations"]),
            }
            for name, members in splits.items()
        },
    }

    print(f"{len(convs)} conversations, {len(groups)} groups, {total} turns "
          f"({total * 2} training strings)\n")
    for name in ("train", "validation", "test"):
        s = payload["splits"][name]
        print(f"  {name:<11} {s['turns']:>4} turns ({s['share']:.0%})  "
              f"{len(s['groups']):>2} groups, {len(s['conversations']):>2} conversations")
    incomplete = [c["id"] for c in convs if c["complete_pairs"] != c["turns"]]
    if incomplete:
        print(f"\n  WARNING incomplete case1/case2 pairs in: {', '.join(incomplete)}")

    # Two rewrites of the same conversation are near-duplicates of each other.
    from collections import Counter
    rewrites = Counter(c["id"].split("-modified")[0] for c in convs if c["modified"])
    twice = [pid for pid, n in rewrites.items() if n > 1]
    if twice:
        print(f"\n  NOTE participant {', '.join(twice)} has more than one modified "
              f"generation. They are in the same split, so nothing leaks, but training\n"
              f"       on both duplicates that conversation - worth confirming with Stiti "
              f"which one counts.")

    if args.show:
        return
    OUT.write_text(json.dumps(payload, indent=2) + "\n")
    print(f"\nwrote {OUT.relative_to(ROOT)} - commit this, and do not regenerate it "
          f"once runs are in the table")


if __name__ == "__main__":
    main()
