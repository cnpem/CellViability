#!/bin/sh
#SBATCH --job-name=cell_viability_analysis
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=4
#SBATCH --partition=short-gpu-small
#SBATCH --gres=gpu:1g.5gb:3
#SBATCH --mem-per-cpu=4G

# Parse command line arguments
while getopts "m:p:h" opt; do
        case $opt in
        m)
                mode=$OPTARG
                ;;
        p)
                plugins_directory=$OPTARG
                ;;
        h)
                echo "Usage: $0 -m [marvin|local] -p [plugins_directory]"
                exit 0
                ;;
        *)
                echo "Invalid option: -$OPTARG" >&2
                echo "Usage: $0 -m [marvin|local] -p [plugins_directory]"
                exit 1
                ;;
        esac
done

# Process plate
if [ "$mode" = "marvin" ]; then
        echo "[==> Processing plate on HPC Marvin"
        singularity run --nv /opt/images/cellprofiler/cellprofiler-4_2_6.sif -c -r -p cell_viability.cppipe -i data -o results --images-per-batch=12
elif [ "$mode" = "local" ]; then
        echo "[==> Processing plate on local machine"
        cellprofiler -c -r -p cell_viability.cppipe -i data -o results --images-per-batch=12 --plugins-directory=${plugins_directory}
else
        echo "Mode not specified or invalid. Use -m marvin or -m local."
        exit 1
fi

# Data mining
echo "[==> Data mining"
python postprocess.py
