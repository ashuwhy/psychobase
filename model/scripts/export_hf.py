"""Cast a finished run's best checkpoint to fp16 for the Hugging Face Hub.

evaluate.py and generate_cases.py load checkpoints in fp16 on the GPU, so this is
the exact model that was scored, at half the size of the fp32 training output.

    python3 model/scripts/export_hf.py model/runs/smollm2-1.7b
"""
import json
import shutil
import sys
from pathlib import Path

import torch
from safetensors.torch import load_file, save_file

run = Path(sys.argv[1])
src, dst = run / "final", run / "hf_fp16"
dst.mkdir(exist_ok=True)

weights = load_file(src / "model.safetensors")
save_file({k: v.to(torch.float16).contiguous() for k, v in weights.items()},
          dst / "model.safetensors", metadata={"format": "pt"})

config = json.loads((src / "config.json").read_text())
config["dtype"] = "float16"
config["use_cache"] = True  # off in training only because of gradient checkpointing
config.pop("transformers.js_config", None)  # inherited from the base repo; names ONNX files we do not ship
(dst / "config.json").write_text(json.dumps(config, indent=2) + "\n")

for name in ("generation_config.json", "tokenizer.json", "tokenizer_config.json", "chat_template.jinja"):
    shutil.copy(src / name, dst / name)
print(f"{len(weights)} tensors -> {dst}")
