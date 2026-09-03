#!/usr/bin/env bash
# One paste, everything needed to write a correct sbatch file. Read-only.
echo "=== scheduler ==="
sinfo -o '%20P %10a %8D %12l %N' 2>/dev/null || echo "sinfo failed"
echo
echo "=== gpu resources per partition ==="
sinfo -o '%20P %N %G' 2>/dev/null | grep -v 'gpu:0' || true
echo
echo "=== what this account may use ==="
sacctmgr -nP show assoc user="$USER" format=Account,Partition,QOS,MaxWall 2>/dev/null || echo "sacctmgr unavailable"
echo
echo "=== queue right now ==="
squeue -o '%.8i %.12P %.10u %.8T %.10M %.6D %R' 2>/dev/null | head -20
echo
echo "=== login node ==="
echo "cuda:   $(ls -d /usr/local/cuda-* 2>/dev/null | tr '\n' ' ')"
echo "python: $(python3 -V 2>&1)"
echo "quota:"; quota -s 2>/dev/null | tail -3 || df -h "$HOME" | tail -1
echo "home:   $HOME"
echo
echo "=== a real GPU, via the scheduler ==="
srun --gres=gpu:1 --time=00:02:00 --pty nvidia-smi 2>&1 | head -14
