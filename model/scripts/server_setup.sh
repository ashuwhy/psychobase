#!/usr/bin/env bash
# Build the training environment on the CSE cluster. Safe to re-run.
#   bash model/scripts/server_setup.sh
set -euo pipefail
cd "$(dirname "$0")/../.."
VENV="$HOME/.venv/psychobase"

# python3-venv is not installed on the login node and there is no sudo, no
# module system and no conda. pip itself works, so bootstrap virtualenv into
# ~/.local and use that instead - it does not need ensurepip.
if [ ! -x "$HOME/.local/bin/virtualenv" ]; then
    pip3 install --user --quiet virtualenv
fi
export PATH="$HOME/.local/bin:$PATH"

if [ ! -x "$VENV/bin/python" ]; then
    rm -rf "$VENV"
    virtualenv --quiet -p python3.10 "$VENV"
fi

# The driver is 580.95, which reports CUDA 13.0, so it accepts any wheel up to
# cu13 - /usr/local/cuda-12.1 on the login node is only the installed toolkit and
# does not constrain this. torch 2.6 is the floor because accelerate's FSDP2 path
# refuses to load below it, and cu124 still ships sm_70 kernels, which matters
# because the V100s are Volta and newer CUDA builds have been dropping them.
"$VENV/bin/pip" install -q --upgrade pip
"$VENV/bin/pip" install -q "torch==2.6.0" --index-url https://download.pytorch.org/whl/cu124
# bitsandbytes is not optional: the 8-bit optimiser states are the difference
# between 26GB and 38GB for the 2B baseline, and the V100s have 32GB.
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
