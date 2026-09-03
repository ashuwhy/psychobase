#!/usr/bin/env bash
# Build the training environment on the CSE cluster. Safe to re-run.
#   bash model/scripts/server_setup.sh
set -euo pipefail
cd "$(dirname "$0")/../.."
VENV="$HOME/.venv/psychobase"

# CUDA 12.1 on the login node, so cu121 wheels. Installing a cu124 torch against
# a 12.1 driver is the usual way this breaks: it imports fine and then fails at
# the first kernel launch, on the GPU node, twenty minutes into a queue wait.
if [ ! -d "$VENV" ]; then
    python3 -m venv "$VENV"
fi
"$VENV/bin/pip" install -q --upgrade pip
"$VENV/bin/pip" install -q torch --index-url https://download.pytorch.org/whl/cu121
"$VENV/bin/pip" install -q transformers accelerate bitsandbytes

echo "=== installed ==="
"$VENV/bin/python" - <<'PY'
import torch, transformers
print("torch       ", torch.__version__, "cuda", torch.version.cuda)
print("transformers", transformers.__version__)
print("gpu visible ", torch.cuda.is_available(), "- False on the login node is expected")
PY

echo
echo "=== smoke test, no GPU needed ==="
"$VENV/bin/python" model/scripts/train.py model/configs/baseline.json --smoke

echo
echo "Environment at $VENV"
echo "Next: sbatch model/scripts/train.sbatch model/configs/baseline.json"
