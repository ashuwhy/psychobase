#!/usr/bin/env bash
#SBATCH --job-name=psychobase-eval
#SBATCH --partition=gpupart_v100
#SBATCH --gres=gpu:1
#SBATCH --cpus-per-task=8
#SBATCH --time=02:00:00
#SBATCH --output=model/runs/slurm-%j.out
#SBATCH --error=model/runs/slurm-%j.out
#
# Score one finished run, or several:
#   sbatch model/scripts/evaluate.sbatch model/runs/baseline
#   sbatch model/scripts/evaluate.sbatch model/runs/baseline model/runs/smollm2-1.7b
set -euo pipefail
cd "$SLURM_SUBMIT_DIR"
export HF_HOME="$HOME/.cache/huggingface"

for RUN in "$@"; do
    echo "=== $RUN ==="
    "$HOME/.venv/psychobase/bin/python" model/scripts/evaluate.py "$RUN"
done
