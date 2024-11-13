#!/bin/sh
#SBATCH --job-name=cell_viability_benchmarking
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=4
#SBATCH --partition=short-gpu-small
#SBATCH --gres=gpu:1g.5gb:3
#SBATCH --mem-per-cpu=4G

usage() {
    echo "Run benchmarking for cell viability pipelines."
    echo "Usage: $0 -m [marvin|local] -p [plugins_directory]"

    echo "Options:"
    echo "  -h    Show this help message."
    echo "  -m [marvin|local]    Mode to run the pipeline. \"marvin\" for HPC Marvin, \"local\" for local machine."
    echo "  -p [plugins_directory]    Path to the plugins directory. Required when mode is local."
    echo " plugins_directory is the path to the \"active_plugins\" directory from the repository: https://github.com/CellProfiler/CellProfiler-plugins.git."
    exit 1
}

# Parse command line arguments
while getopts "m:p:h" opt; do
    case $opt in
    m) mode=$OPTARG ;;
    p) plugins_directory=$OPTARG ;;
    h) usage ;;
    *) usage ;;
    esac
done

# Check if mode is set
if [ -z "$mode" ]; then
    echo "Mode not specified."
    usage
fi

run_pipeline() {
    local pipeline=$1
    local output_dir=$2
    local extra_args=$3

    echo "> Running $pipeline pipeline"
    singularity run --nv /opt/images/cellprofiler/cellprofiler-4_2_6.sif -c -r -p pipelines/$pipeline -i data -o results/$output_dir --images-per-batch=12 $extra_args
}        cppipe" "conventional"
    run_pipeline "cell_viability_cellpose.cppipe" "cellpose"
    ;;
local)
    if [ -z "$plugins_directory" ]; then
        echo "Plugins directory must be specified with -p when mode is local."
        exit 1
    fi
    echo "[==> Processing plate on local machine"
    run_pipeline "cell_viability_conventional.cppipe" "conventional" "--plugins-directory=${plugins_directory}"
    run_pipeline "cell_viability_cellpose.cppipe" "cellpose" "--plugins-directory=${plugins_directory}"
    ;;
*)
    echo "Invalid mode: $mode"
    usage
    ;;
esac

# Data mining and visualization
echo "[==> Data mining and visualization"
if [ -f "benchmarking.py" ]; then
    python benchmarking.py
else
    echo "benchmarking.py not found. Skipping data mining and visualization."
fi
