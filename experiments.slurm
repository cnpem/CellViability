#!/bin/sh
#SBATCH --job-name=CellViability
#SBATCH --output=slurm-%j.out
#SBATCH --error=slurm-%j.err
#SBATCH --partition=lbc
#SBATCH --nodelist=dgpu01
#SBATCH --exclusive
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=32
#SBATCH --mem-per-cpu=4GB
#SBATCH --gres=gpu:1
#SBATCH --time=12:00:00

module load uv
make experiments
