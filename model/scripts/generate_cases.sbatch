#!/usr/bin/env bash
#SBATCH --job-name=psychobase-cases
#SBATCH --partition=gpupart_v100
#SBATCH --gres=gpu:1
#SBATCH --cpus-per-task=4
#SBATCH --time=00:30:00
#SBATCH --output=model/runs/slurm-%j.out
#SBATCH --error=model/runs/slurm-%j.out
#
# One checkpoint over one or more cases files:
#   sbatch model/scripts/generate_cases.sbatch model/runs/<run_id> \
#       model/eval_cases/stage2_cases.json model/eval_cases/ashutosh_conversation.json
#
# Inference only - a 1.7B model in fp16 is about 3.5GB, so it does not need a
# V100. When gpupart_v100 is backed up, `sbatch -p gpupart_p100 ...` overrides
# the partition above.
set -euo pipefail
cd "$SLURM_SUBMIT_DIR"
export HF_HOME="$HOME/.cache/huggingface"

RUN="$1"
shift
for CASES in "$@"; do
    "$HOME/.venv/psychobase/bin/python" model/scripts/generate_cases.py "$RUN" "$CASES"
done
