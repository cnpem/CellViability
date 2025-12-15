#!/bin/sh
#SBATCH --job-name=CellViability
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=32
#SBATCH --partition=short-gpu-small
#SBATCH --gres=gpu:1g.5gb:1
#SBATCH --mem-per-cpu=4GB
#SBATCH --array=0-3
#SBATCH --time=24:00:00

module load uv
time uv run CellViability --config config.json --index=${SLURM_ARRAY_TASK_ID} --npy --instances --basedir results --verbose
