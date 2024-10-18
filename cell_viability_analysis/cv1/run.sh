#!/bin/sh
#SBATCH --job-name=cv1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=4
#SBATCH --partition=short-gpu-small
#SBATCH --gres=gpu:1g.5gb:3
#SBATCH --mem-per-cpu=4G

time singularity run --nv /opt/images/cellprofiler/cellprofiler-4_2_6.sif -p cv1.cppie -c -r 
