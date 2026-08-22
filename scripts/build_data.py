#!/usr/bin/env python3
"""Turn the supplied CSV + JSON into what the frontend actually needs.

Two inputs per participant:

  public/data/raw_csv/participantGrouped<ID>data.csv        raw signal samples
  public/data/json/output_participantGrouped<ID>data_full_data.json   turns

Two things about the raw CSV are worth knowing before reading this:

1. It is one row per conversation turn, not a stream of samples. The timestamp
   column is a range, "2026-05-04T19:33:00-2026-05-04T19:34:00" (with an en-dash),
   and every signal column holds a small array of samples taken inside it.
   To draw a full-conversation trend we flatten those arrays onto a real time
   axis, spacing each row's samples evenly across its own window.

2. The highlight interval for a turn is NOT that turn's row window. The
   physiological summary looks backwards - turn 4 sits at 19:38 and its summary
   says "over the past 5 minutes", so the band starts at 19:33. That look-back
   grows through the conversation and then holds at 6 minutes, which is why the
   interval has to be read per turn rather than assumed.

Output: public/data/build/index.json plus one <context_id>.json per context.
"""

import ast
import csv
import json
import re
from datetime import datetime, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RAW = ROOT / "public" / "data" / "raw_csv"
JSON_DIR = ROOT / "public" / "data" / "json"
OUT = ROOT / "public" / "data" / "build"

# The five charted signals. The brief listed ACT_CLASS as the fifth, but it holds
# category strings ('generic', 'still') rather than numbers; Stiti confirmed on
# 15 Aug that the fifth graph is ACT_COUNT.
SIGNALS = [
    {"key": "EDA", "label": "Electrodermal activity", "unit": "uS", "kind": "numeric"},
    {"key": "PR", "label": "Pulse rate", "unit": "bpm", "kind": "numeric"},
    {"key": "SkinTemp", "label": "Skin temperature", "unit": "degC", "kind": "numeric"},
    {"key": "ACCEL", "label": "Acceleration", "unit": "g", "kind": "numeric"},
    {"key": "ACT_COUNT", "label": "Activity count", "unit": "counts", "kind": "numeric"},
]

# Carried in `series` but not charted - useful for annotating a turn ("still" vs
# "walking") without becoming a sixth graph.
EXTRA_SERIES = [
    {"key": "ACT_CLASS", "label": "Activity class", "unit": "", "kind": "categorical"},
]

# "Over the past 2 minutes", "across the last 6 minutes", "the first minute", ...
LOOKBACK_RE = re.compile(
    r"(?:past|last|previous|over the|across the|during the|within the)\s+"
    r"(\d+|one|two|three|four|five|six|seven|eight|nine|ten)\s*-?\s*minute",
    re.I)
FIRST_MINUTE_RE = re.compile(r"\bfirst minute\b", re.I)
WORD_NUMBERS = {"one": 1, "two": 2, "three": 3, "four": 4, "five": 5,
                "six": 6, "seven": 7, "eight": 8, "nine": 9, "ten": 10}


def parse_range(cell):
    """'2026-05-04T19:33:00-2026-05-04T19:34:00' -> (start, end) datetimes."""
    parts = re.split(r"–|—|(?<=\d{2}:\d{2}:\d{2})-(?=\d{4})", cell.strip())
    parts = [p for p in parts if p]
    start = datetime.fromisoformat(parts[0])
    end = datetime.fromisoformat(parts[1]) if len(parts) > 1 else start
    return start, end


def parse_array(cell):
    """CSV holds python-literal arrays: '[4.13, 3.99]' or "['generic', 'still']"."""
    if cell is None or cell.strip() == "":
        return []
    try:
        value = ast.literal_eval(cell)
    except (ValueError, SyntaxError):
        return []
    if not isinstance(value, list):
        value = [value]
    return value


def clean(value):
    """NaN is not valid JSON - emit null so the chart can break the line."""
    if isinstance(value, float) and value != value:
        return None
    if isinstance(value, str) and value.lower() == "nan":
        return None
    return value


def jsonable(value):
    """Strip NaN and infinities anywhere in the structure, not just in readings.

    Python writes float('nan') as a bare NaN, which JSON.parse rejects outright,
    taking the whole page down with "Unexpected token 'N'". The source files
    carry NaN in more than the signal arrays - participant_full_id is NaN for
    the second session of 11_2, for instance - so the whole payload is walked
    rather than trusting field-by-field cleaning.
    """
    if isinstance(value, float):
        return value if value == value and value not in (float("inf"), float("-inf")) else None
    if isinstance(value, dict):
        return {k: jsonable(v) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        return [jsonable(v) for v in value]
    return value


def dump(payload, path, **kwargs):
    """Write JSON, refusing to emit anything JSON.parse would reject."""
    path.write_text(json.dumps(jsonable(payload), allow_nan=False, **kwargs), encoding="utf-8")


def lookback_minutes(summary_text):
    """Minutes the summary looks back over, or None when it cannot be read."""
    if not summary_text:
        return None
    if FIRST_MINUTE_RE.search(summary_text):
        return 1
    match = LOOKBACK_RE.search(summary_text)
    if not match:
        return None
    token = match.group(1).lower()
    return int(token) if token.isdigit() else WORD_NUMBERS.get(token)


def physio_summary(turn):
    """The 'Physiological Signals: ...' block out of training_string_case2."""
    text = turn.get("training_string_case2", "")
    match = re.search(r"Physiological Signals:\s*(.*?)\s*(?=\n###|\Z)", text, re.S)
    return match.group(1).strip() if match else ""


def row_windows(rows):
    """Work out the real [start, end] each CSV row covers.

    Two shapes turn up in the supplied files. Most rows carry an explicit range,
    "19:33:00-19:34:00". Others carry a single timestamp, "18:00:00", and still
    hold several samples - participant 8 has three per row, three minutes apart.
    Treating those as zero-length would stamp every sample in the row on the same
    instant, stacking points on top of each other and flattening the trend, so a
    row with no end borrows the next row's start. The final row reuses the median
    gap, since there is nothing after it to measure against.
    """
    starts, ends = [], []
    for row in rows:
        start, end = parse_range(row["timestamp"])
        starts.append(start)
        ends.append(end if end > start else None)

    gaps = [(starts[i + 1] - starts[i]).total_seconds()
            for i in range(len(starts) - 1) if starts[i + 1] > starts[i]]
    median_gap = sorted(gaps)[len(gaps) // 2] if gaps else 60.0

    for i, end in enumerate(ends):
        if end is None:
            nxt = starts[i + 1] if i + 1 < len(starts) else None
            ends[i] = nxt if nxt and nxt > starts[i] else starts[i] + timedelta(seconds=median_gap)
    return list(zip(starts, ends))


def build_series(rows):
    """Flatten per-row sample arrays onto a real time axis.

    A row covering 19:33-19:34 with two samples puts them at the 1/4 and 3/4
    marks of that minute rather than both on the boundary, so consecutive rows
    do not stack points on the same timestamp.
    """
    channels = SIGNALS + EXTRA_SERIES
    series = {s["key"]: [] for s in channels}
    for row, (start, end) in zip(rows, row_windows(rows)):
        span = (end - start).total_seconds()
        for signal in channels:
            values = parse_array(row.get(signal["key"], ""))
            if not values:
                continue
            step = span / len(values) if span else 0
            for i, value in enumerate(values):
                at = start + timedelta(seconds=step * (i + 0.5)) if step else start
                series[signal["key"]].append({"t": at.isoformat(), "v": clean(value)})
    for key in series:
        series[key].sort(key=lambda p: p["t"])
    return series


def build_context(csv_path, json_path):
    rows = list(csv.DictReader(csv_path.open(encoding="utf-8")))
    sessions = json.loads(json_path.read_text(encoding="utf-8"))
    turns_json = [t for s in sessions for t in s["turns"]]

    series = build_series(rows)
    all_points = [p["t"] for pts in series.values() for p in pts]
    domain = [min(all_points), max(all_points)] if all_points else [None, None]

    # Turns whose stated look-back disagrees with the dynamic scheme Stiti
    # described (1, 2, 3 ... holding at 6) are worth surfacing rather than
    # silently trusting, since that scheme drives the highlight.
    mismatches = []
    turns = []
    for i, turn in enumerate(turns_json, 1):
        summary = physio_summary(turn)
        minutes = lookback_minutes(summary)
        at = datetime.fromisoformat(turn["timestamp"])
        # Look back from the turn's own timestamp. Fall back to the row window
        # when the summary has no readable interval, rather than guessing.
        if minutes:
            start, end = at - timedelta(minutes=minutes), at
            # The opening turn looks back past the start of the recording, so slide
            # the band forward instead of highlighting empty axis.
            if domain[0] and start.isoformat() < domain[0]:
                start = datetime.fromisoformat(domain[0]).replace(microsecond=0)
                end = start + timedelta(minutes=minutes)
            interval = {"start": start.isoformat(), "end": end.isoformat(),
                        "minutes": minutes, "source": "summary"}
        elif i - 1 < len(rows):
            start, end = row_windows(rows)[i - 1]
            interval = {"start": start.isoformat(), "end": end.isoformat(),
                        "minutes": round((end - start).total_seconds() / 60),
                        "source": "csv_row"}
        else:
            interval = None
        expected = min(i, 6)
        if minutes and minutes != expected:
            mismatches.append((i, minutes, expected))
        turns.append({
            "turn": i,
            "timestamp": turn["timestamp"],
            # NaN where a session has no id (11_2's second session). The field is
            # a string downstream, so make it an empty one rather than a null.
            "participant_full_id": (turn.get("participant_full_id")
                                    if isinstance(turn.get("participant_full_id"), str) else ""),
            "user_text": turn.get("user_text", ""),
            "ai_text": turn.get("ai_text", ""),
            "strategy": (turn.get("strategy") or "").strip(),
            "physio_summary": summary,
            "stress_score": turn.get("stress_score"),
            "stress_level": turn.get("stress_level"),
            "interval": interval,
        })
    return {"signals": SIGNALS, "domain": domain, "series": series, "turns": turns,
            "interval_mismatches": mismatches}


def context_names():
    """Optional context_id -> display name map, from Stiti's Google doc.

    The JSON files carry an empty `context` field for all 749 turns, so the
    selection screen has no scenario name of its own. Drop the mapping into
    public/data/context_names.json and it flows through to index.json; until
    then cards fall back to the participant id.
    """
    path = ROOT / "public" / "data" / "context_names.json"
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def discover():
    """Pair every CSV with its JSON, keeping originals and modified versions apart.

    Stiti sends two kinds of file per participant:

      participantGrouped8data.csv                 + output_participantGrouped8data_full_data.json
      participantGrouped8data_modified_phyS.csv   + output_participantGrouped8data_modified_phyS_full_data.json

    The modified ones are better regenerations of a conversation we already have.
    They are additional contexts rather than replacements - the brief is to add
    them without removing the originals - so a modified variant gets its own
    context id, "8-modified", and the original "8" is left alone. The modifier
    suffix varies (_modified, _modified_phyS, _modified_phyS_context), so it is
    captured rather than hard-coded.

    Pairing is by the *exact* suffix, not just "is this modified or not" -
    participant 1 once had a CSV suffixed "_modified" matched against a JSON
    suffixed "_modified_phyS" purely because both were "modified", which
    silently paired files that were never meant to go together. Exact-suffix
    matching means a suffix with no counterpart on the other side is reported
    as skipped instead of guessed at.
    """
    csvs, jsons = {}, {}
    for path in RAW.glob("participantGrouped*.csv"):
        m = re.match(r"participantGrouped(.+?)data(_modified[a-zA-Z_]*)?\.csv$", path.name)
        if m:
            csvs[(m.group(1), m.group(2) or "")] = path
    for path in JSON_DIR.glob("output_participantGrouped*.json"):
        m = re.match(r"output_participantGrouped(.+?)data(_modified[a-zA-Z_]*)?_full_data\.json$",
                     path.name)
        if m:
            jsons[(m.group(1), m.group(2) or "")] = path

    contexts, skipped = [], []
    for key in sorted(csvs, key=lambda k: (natural(k[0]), k[1])):
        pid, suffix = key
        is_modified = bool(suffix)
        if key not in jsons:
            skipped.append(pid + ("-modified" if is_modified else ""))
            continue
        contexts.append((pid + ("-modified" if is_modified else ""), csvs[key], jsons[key],
                         pid, is_modified))
    return contexts, skipped


def natural(pid):
    """'11_1' -> (11, 1) so contexts sort 8, 11, 11_1 rather than lexically."""
    return tuple(int(part) for part in pid.split("_"))


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    names = context_names()
    contexts, skipped = discover()

    # One index row per base participant, holding both variants, rather than a
    # separate top-level card for "8" and "8-modified" - they are the same
    # conversation, so the selection screen should not show it twice.
    groups = {}
    for cid, csv_path, json_path, base_id, is_modified in contexts:
        context = build_context(csv_path, json_path)
        dump(context, OUT / f"{cid}.json")
        variant = {
            "id": cid,
            "label": "Modified" if is_modified else "Original",
            "participant_id": context["turns"][0]["participant_full_id"] if context["turns"] else "",
            "turn_count": len(context["turns"]),
            "start": context["domain"][0],
            "end": context["domain"][1],
        }
        group = groups.setdefault(base_id, {"context_id": base_id, "name": names.get(base_id, ""),
                                             "variants": []})
        group["variants"].append(variant)
        mismatched = len(context["interval_mismatches"])
        print(f"  {cid:<14} {len(context['turns']):>3} turns, "
              f"{len(context['series']['EDA']):>3} EDA points"
              + (f", {mismatched} off the 1-2-3-..-6 scheme" if mismatched else ""))

    index = [groups[pid] for pid in sorted(groups, key=natural)]
    for group in index:
        group["variants"].sort(key=lambda v: v["label"] != "Original")
    dump(index, OUT / "index.json", indent=1)

    n_contexts = len(index)
    n_variants = sum(len(g["variants"]) for g in index)
    n_mod = sum(1 for g in index for v in g["variants"] if v["label"] == "Modified")
    print(f"\n{n_contexts} contexts, {n_variants} variants "
          f"({n_variants - n_mod} original, {n_mod} modified) -> {OUT}")
    if skipped:
        print(f"  skipped, no matching JSON: {', '.join(skipped)}")
    unnamed = [g["context_id"] for g in index if not g["name"]]
    if unnamed:
        print(f"  no context name yet: {', '.join(unnamed)}")


if __name__ == "__main__":
    main()
