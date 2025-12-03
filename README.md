# Cell Viability Assay

This repository contains the source code for analyzing cell viability assays using high-content screening (HCS) images. The pipeline includes image processing and data mining for quantitative analysis of the number of cells in each image.

## Installation

To install via pip, run the following command:

```bash
pip install CellViability
```

To install the developmental version, clone the repository and run:

```bash
git clone https://github.com/cnpem/CellViability.git
cd CellViability
make install
```

## Usage

To run the analysis for all cell viability assays (i.e., drug screening), use the following command:

```bash
CellViability --config path/to/config.json --npy --instances --basedir results/ --verbose
```

Optional flags:

* `--npy`: saves the results in a NumPy binary file
* `--instances`: saves segmented images.
* `--basedir`: specifies the directory where results will be saved.
* `--verbose`: enables detailed, step-by-step logging.

To run a specific cell viability assay, use the following command:

```bash
CellViability --config path/to/config.json --index <index> --npy --instances --basedir results/ --verbose
```

* `--index <index>`: selects a single condition (0-based index) from the list defined in the `--config` file.

## Authors

* Ana A. S. Iacia
* Jacqueline F. Shimizu
* [João V. S. Guerra](https://github.com/jvsguerra)
* [José G. C. Pereira](https://github.com/zgcarvalho)
* [Kayllany L. S. Oliveira](https://github.com/KayllanyLara)
* [Pablo S. Silva](https://github.com/wapablos)
* Rafael E. Marques
* Thayná M. Avelino

## License

This software is licensed under the terms of the GNU General Public License version 3 (GPL3) and is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
