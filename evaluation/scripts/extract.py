#!/usr/bin/env python3
"""Step 1 of the pipeline: parse a participant JSON and emit the working CSVs.

Outputs (per participant, into out/<participant>/):
  turns_input.csv   - turn, user_text, physio_signals  (input for the MASTER prompt)
  raw_physio.csv    - turn, EDA, PR, SkinTemp, ACCEL, ACT_CLASS, ACT_COUNT, stress
                      (input for the physio-summarizer prompt)
  original_ai.csv   - turn, strategy, ai_text          (baseline for the eval prompt)

Nothing here mutates the source JSON - the email is explicit that the JSON stays
untouched until the scores are verified.
"""

import argparse
import csv
import json
import re
from pathlib import Path

# "Physiological Signals:" line inside training_string_case2, up to the next
# "### " section header. DOTALL so multi-sentence summaries survive intact.
PHYSIO_RE = re.compile(r"Physiological Signals:\s*(.*?)\s*(?=\n###|\Z)", re.DOTALL)


def physio_of(turn):
    m = PHYSIO_RE.search(turn["training_string_case2"])
    return m.group(1).strip() if m else ""


def fmt(vals):
    """Raw channel -> compact 'a -> b' / 'x' / 'not reported' string."""
    if not vals:
        return "not reported"
    if isinstance(vals, (int, float)):
        return str(vals)
    uniq = list(dict.fromkeys(vals))
    return " -> ".join(str(v) for v in uniq) if len(uniq) > 1 else str(uniq[0])


def act_class(turn):
    return turn.get("physio_summary_per_channel", {}).get("ACT_CLASS", "not reported")


def write(path, header, rows):
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(header)
        w.writerows(rows)
    print(f"  wrote {path.name} ({len(rows)} rows)")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("json_file")
    ap.add_argument("-o", "--outdir", default="out")
    args = ap.parse_args()

    src = Path(args.json_file)
    sessions = json.loads(src.read_text(encoding="utf-8"))

    # Turns are numbered continuously across sessions; session_id rides along so a
    # multi-session file (e.g. 11_2) stays traceable back to its source.
    turns = [(s["session_id"], t) for s in sessions for t in s["turns"]]
    outdir = Path(args.outdir) / src.stem.replace("output_participantGrouped", "P").replace(
        "data_full_data", ""
    )
    outdir.mkdir(parents=True, exist_ok=True)
    print(f"{src.name}: {len(sessions)} session(s), {len(turns)} turns -> {outdir}")

    write(
        outdir / "turns_input.csv",
        ["turn", "session_id", "user_text", "physio_signals"],
        [[i, sid, t["user_text"], physio_of(t)] for i, (sid, t) in enumerate(turns, 1)],
    )

    # Stiti's note: the shortening prompt only needs timestamp, raw_physio and the
    # stress score - so this is exactly what gets handed over, nothing more.
    write(
        outdir / "raw_physio.csv",
        ["turn", "session_id", "timestamp", "EDA_uS", "PR_bpm", "SkinTemp_degC", "ACCEL_g",
         "ACT_COUNT", "ACT_CLASS", "stress_score", "stress_level"],
        [
            [
                i,
                sid,
                t.get("timestamp", ""),
                fmt(t["raw_physio"].get("EDA")),
                fmt(t["raw_physio"].get("PR")),
                fmt(t["raw_physio"].get("SkinTemp")),
                fmt(t["raw_physio"].get("ACCEL")),
                fmt(t["raw_physio"].get("ACT_COUNT")),
                act_class(t),
                t.get("stress_score"),
                t.get("stress_level") or "not reported",
            ]
            for i, (sid, t) in enumerate(turns, 1)
        ],
    )

    write(
        outdir / "original_ai.csv",
        ["turn", "session_id", "strategy", "ai_text"],
        [[i, sid, t.get("strategy", ""), t["ai_text"]] for i, (sid, t) in enumerate(turns, 1)],
    )


if __name__ == "__main__":
    main()
