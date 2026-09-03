#!/usr/bin/env bash
#SBATCH --job-name=psychobase-fsdp
#SBATCH --partition=gpupart_v100
#SBATCH --gres=gpu:2
#SBATCH --cpus-per-task=8
#SBATCH --time=08:00:00
#SBATCH --output=model/runs/slurm-%j.out
#SBATCH --error=model/runs/slurm-%j.out
#
# Both V100s on gnode1, for the configs that carry a "distributed" block.
#   sbatch model/scripts/train_fsdp.sbatch model/configs/smollm3-3b.json
#
# Single-card runs use train.sbatch. Do not run a 1.7B config through this one:
# sharding changes the reduction order and would make it incomparable with the
# rest of the table for no benefit.
set -euo pipefail
CONFIG="${1:?usage: sbatch train_fsdp.sbatch model/configs/<name>.json}"
cd "$SLURM_SUBMIT_DIR"
mkdir -p model/runs

echo "job $SLURM_JOB_ID on $(hostname), config $CONFIG"
nvidia-smi --query-gpu=name,memory.total --format=csv

export HF_HOME="$HOME/.cache/huggingface"
export OMP_NUM_THREADS=8
mkdir -p "$HF_HOME"

"$HOME/.venv/psychobase/bin/torchrun" --nproc_per_node=2 --master_port=29513 \
    model/scripts/train.py "$CONFIG"
