# Cell viability assay

This repository contains the source code for analyzing cell viability assays using high-content screening (HCS) images. The pipeline includes image processing and data mining for quantitative analysis of the number of cells in each image.

## Images

The images were generated from a phenotypic assay of VERO CCL81 cells provided by Dr. Rafael E. Marques (LNBio), which were infected with the Mayaro virus and treated with the vehicle DMSO, alongside non-infected controls. The cells were stained with the fluorophore Hoechst 33342, a DNA marker, and the images were acquired using the Operetta microscope (10x magnification).

## Analysis

The images were processed using open-source tools, such as CellProfiler, for image processing analysis, and then data mined in Python for quantitative analysis. The custom CellProfiler pipeline included pre-processing, segmentation of nuclei, and calculation of metrics (number of cells).

To run the pipeline, follow the instructions below:

1. Install [CellProfiler](https://cellprofiler.org/releases/) and the required [plugins](https://github.com/cnpem/lnbio-bioimage-analysis/blob/main/cellprofiler/INSTALLATION.md#cellprofiler-plugins).

2. Run the pipeline and data mining using the `run.sh` script:

```bash
# Running on HPC marvin machine
sbatch run.sh -m marvin
```

or

```bash
# Running on local machine
bash run.sh -m local -p /path/to/CellProfiler-plugins/active_plugins
```

The output files will be saved in the `results` directory and will include the following files:

```bash
results/
├── summary.csv                   # Summary of the number of cells per well
├── Experiment.csv                # Raw data of the number of cells per image (CellProfiler output)
├── Nuclei.csv                    # Raw data of the segmented nuclei per image (CellProfiler output)
├── Image.csv                     # Raw information per image (CellProfiler output)
└── plate_map/
    └── number_of_cells.html      # Interactive visualization of the number of cells per well
```

### Developers

- [Daniel C. Vieira](https://github.com/Daniel-debug-creator)
- [João V. S. Guerra](https://github.com/jvsguerra)
- [José G. C. Pereira](https://github.com/zgcarvalho)
- [Kayllany L. S. Oliveira](https://github.com/KayllanyLara)

## License

This software is licensed under the terms of the GNU General Public License version 3 (GPL3) and is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
