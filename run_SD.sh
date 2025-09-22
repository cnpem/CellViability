#!/bin/sh
#SBATCH --job-name=SD
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=4
#SBATCH --partition=short-gpu-small
#SBATCH --gres=gpu:1g.5gb:1
#SBATCH --mem-per-cpu=4GB
#SBATCH --output=Sample_1_1_%j.out
#SBATCH --error=Sample_1_1_%j.err

echo "Job started at $(date)"
source SD/bin/activate
python /home/kayllany.oliveira/remote-repos/CellViability/SD.py
sleep 10  # wait 10 seconds
echo "Job ended at $(date)"