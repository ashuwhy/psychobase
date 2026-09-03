#!/usr/bin/env bash
#SBATCH --job-name=psychobase
#SBATCH --gres=gpu:1
#SBATCH --cpus-per-task=8
#SBATCH --time=04:00:00
#SBATCH --output=model/runs/slurm-%j.out
#SBATCH --error=model/runs/slurm-%j.out
#
# Submit one config:
#   sbatch model/scripts/train.sbatch model/configs/smollm2-1.7b.json
#
# Add --partition=<name> once cluster_probe.sh says what the partitions are
# called. Left out deliberately rather than guessed, because a wrong partition
# name fails at submit time with a message nobody reads carefully.
set -euo pipefail
CONFIG="${1:?usage: sbatch train.sbatch model/configs/<name>.json}"
cd "$SLURM_SUBMIT_DIR"
mkdir -p model/runs

echo "job $SLURM_JOB_ID on $(hostname), config $CONFIG"
nvidia-smi --query-gpu=name,memory.total,memory.used --format=csv

# HF_HOME on scratch, not the NFS home: three model families at 2-6GB each will
# blow a student quota, and every node re-downloading is slower than sharing.
export HF_HOME="${SCRATCH:-$HOME}/.cache/huggingface"
mkdir -p "$HF_HOME"

"$HOME/.venv/psychobase/bin/python" model/scripts/train.py "$CONFIG"
