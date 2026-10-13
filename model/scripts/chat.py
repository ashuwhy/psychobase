#!/usr/bin/env python3
"""Talk to a fine-tuned checkpoint in the terminal, one turn at a time.

    python3 model/scripts/chat.py ashuwhy/psychobase-smollm2-1.7b
    python3 model/scripts/chat.py model/runs/smollm2-1.7b/final

Type the user's message, then the physiological summary. The summary may run
over several lines and ends at an empty line; an empty line straight away
means no summary, which the model sees as "Not Available", the same as a
case1 training string. Ctrl-D or "quit" ends the session.

Every turn is built exactly the way generate_cases.py builds its CSV rows -
same header, same Input layout, greedy, 300 new tokens - so typing a case from
model/eval_cases/ here answers what that case's CSV row answers. That holds on
the hardware the CSVs came from. On Apple MPS, one prompt at a time, 45 of the
52 rows match; fp16 rounds differently there, and once one greedy token flips
the rest of the answer follows it. Each turn stands alone: training strings
carry no history, so earlier turns are not fed back in.
"""

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from dataset import load  # noqa: E402
from evaluate import RESPONSE_MARKER, parse  # noqa: E402
from generate_cases import physio_field  # noqa: E402


def read_physio():
    lines = []
    while True:
        line = input("... " if lines else "Physio> ")
        if not line.strip():
            return physio_field("\n".join(lines) or "Not Available")
        lines.append(line)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("model", help="a checkpoint directory or a Hugging Face repo id")
    args = ap.parse_args()

    header = load("test")[0].case1.partition("### Input:")[0]

    import torch
    from transformers import AutoModelForCausalLM, AutoTokenizer

    # fp16 wherever the hardware has it, because the scored model is the fp16 one
    # on the Hub; a CPU falls back to fp32.
    if torch.cuda.is_available():
        device, dtype = "cuda", torch.float16
    elif torch.backends.mps.is_available():
        device, dtype = "mps", torch.float16
    else:
        device, dtype = "cpu", torch.float32
    tok = AutoTokenizer.from_pretrained(args.model)
    if tok.pad_token is None:
        tok.pad_token = tok.eos_token
    model = AutoModelForCausalLM.from_pretrained(args.model, dtype=dtype).to(device)
    model.eval()
    print(f"loaded {args.model} on {device} ({str(dtype).removeprefix('torch.')})")
    print("Physio: end with an empty line; an empty line straight away = Not Available\n")

    while True:
        try:
            text = input("You> ").strip()
            if text.lower() in ("quit", "exit"):
                break
            if not text:
                continue
            physio = read_physio()
        except EOFError:
            print()
            break
        prompt = (f"{header}### Input:\nText: {text}\n"
                  f"Physiological Signals: {physio}\n\n{RESPONSE_MARKER}")
        enc = tok(prompt, return_tensors="pt").to(device)
        with torch.no_grad():
            out = model.generate(**enc, max_new_tokens=300, do_sample=False,
                                 num_beams=1, pad_token_id=tok.pad_token_id)
        raw = tok.decode(out[0][enc["input_ids"].shape[1]:], skip_special_tokens=True)
        strategy, response = parse(raw)
        print(f"\nStrategy: {strategy or '(none)'}\nResponse: {response or raw.strip()}\n")


if __name__ == "__main__":
    main()
