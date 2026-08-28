#!/usr/bin/env python3
"""Task 5: write the verified summaries, strategies and responses into the JSON.

Replaces the "Physiological Signals", "Strategy" and "Response" parts of
training_string_case2 with the reworked versions in scripts/data/p<id>.py,
leaving every other field - including training_string_case1, ai_text and the
turn-level strategy - exactly as supplied.

Two format details matter:

* The shortened summaries carry a trailing <EOS> because that was the
  summariser's own output contract. Inside training_string_case2 the <EOS>
  belongs at the very end of the string only, so it is stripped from the
  summary before embedding.
* The instruction header and the "Text:" line are preserved byte for byte;
  only the three named parts change.
"""

import importlib.util
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "physio-viz" / "public" / "data" / "json"
OUT = ROOT / "step5"

# "### Input:\nText: ...\nPhysiological Signals: <summary>\n\n### Response:\n
#  Strategy: <s>\n\nResponse: <r><EOS>"
CASE2 = re.compile(
    r"(?P<head>.*?Physiological Signals:\s*)(?P<physio>.*?)"
    r"(?P<mid>\n\n### Response:\nStrategy:\s*)(?P<strategy>.*?)"
    r"(?P<gap>\n\nResponse:\s*)(?P<response>.*?)(?P<tail><EOS>\s*)$",
    re.S)


def load_data(pid):
    path = ROOT / "scripts" / "data" / f"p{pid.lower()}.py"
    spec = importlib.util.spec_from_file_location(f"data_p{pid}", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def rebuild(case2, physio, strategy, response):
    m = CASE2.match(case2)
    if not m:
        raise ValueError("training_string_case2 did not match the expected shape")
    # The template already supplies the "Physiological Signals: " label, and the
    # summary carries its own copy plus a trailing <EOS> from the summariser's
    # output contract. Both would otherwise be duplicated inside the string.
    physio = physio.strip()
    if physio.startswith("Physiological Signals:"):
        physio = physio[len("Physiological Signals:"):].lstrip()
    if physio.endswith("<EOS>"):
        physio = physio[: -len("<EOS>")].rstrip()
    return (m.group("head") + physio + m.group("mid") + strategy
            + m.group("gap") + response + m.group("tail"))


def main(pids):
    OUT.mkdir(exist_ok=True)
    for pid in pids:
        data = load_data(pid)
        name = f"output_participantGrouped{pid}data_full_data.json"
        sessions = json.loads((SRC / name).read_text(encoding="utf-8"))

        n = 0
        for session in sessions:
            for turn in session["turns"]:
                n += 1
                strategy, response = data.NEW_RESPONSE[n]
                turn["training_string_case2"] = rebuild(
                    turn["training_string_case2"], data.PHYSIO_SHORT[n], strategy, response)

        expected = len(data.NEW_RESPONSE)
        if n != expected:
            raise SystemExit(f"{pid}: JSON has {n} turns but the rework has {expected}")

        (OUT / name).write_text(json.dumps(sessions, indent=4, ensure_ascii=False),
                                encoding="utf-8")
        print(f"  {pid:<6} {n} turns rewritten -> step5/{name}")


if __name__ == "__main__":
    main(sys.argv[1:] or ["11", "11_1", "11_2", "11_3"])
