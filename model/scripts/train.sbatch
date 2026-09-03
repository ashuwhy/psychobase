#!/usr/bin/env bash
#SBATCH --job-name=psychobase
#SBATCH --partition=gpupart_v100
#SBATCH --gres=gpu:1
#SBATCH --cpus-per-task=8
#SBATCH --time=08:00:00
#SBATCH --output=model/runs/slurm-%j.out
#SBATCH --error=model/runs/slurm-%j.out
#
# Submit one config:
#   sbatch model/scripts/train.sbatch model/configs/smollm2-1.7b.json
#
# gpupart_v100 is gnode1, the only node on the cluster with enough memory to
# fully fine-tune anything in our size range: 2x Tesla V100-PCIE-32GB. The other
# partitions are P100 16GB (gnode2-5) and Quadro P4000 8GB (gnode6-8), and the
# P4000s cannot hold a 1B model in fp16 full fine-tuning at all.
#
# No card here is Ampere, so bf16 is unavailable cluster-wide - compute
# capability tops out at 7.0. Every run therefore trains fp16 with fp32 master
# weights, about 12 bytes/param, which is what train.py selects on its own.
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
