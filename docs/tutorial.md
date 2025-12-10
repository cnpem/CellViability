# CellViability Execution Tutorial

This tutorial provides a complete guide, from preparing the files to running the full analysis using the `uv run CellViability` command.

---

## 1. Preparing the Directory

Before running the system, ensure that the folder structure is correctly organized. The main directory should contain:

```
./
├── screen/
│   ├── P1/
│   │   ├── 001001-1-001001001.tif
│   │   ├── 001002-1-001001001.tif
│   ├── P2/
│   └── ...
├── results/
└── config.json
```

### What You Must Ensure

* All images must be in `.tif` format following the naming pattern:

  * `001001` — the well (row and column)
  * `1` — the field number
  * `001001001` — extra information (e.g., timepoint, channel, z-stack)

* The `config.json` file must contain the required configuration parameters.

> **Note:** The detailed content of `config.json` will be explained in another section. This part focuses only on execution.

---

## 2. Installing and Running with `uv`

When the CellViability package is installed, the environment is already configured. This allows you to run the command directly:

```bash
uv run CellViability --config config.json --instances --npy --verbose
```

### What This Command Does

* Loads the configuration file (`--config config.json`).
* Generates instance masks as `.png` files (`--instances`).
* Generates masks as `.npy` files (`--npy`).
* Prints detailed execution information (`--verbose`).
* Saves outputs inside the `results/` folder (default behavior).

---

## 3. Understanding the Available Options

Running `uv run CellViability --help` shows all available options. Here are the main ones:

### Main Options

* **--config**: path to the JSON configuration file (required).
* **--instances**: saves segmentation masks as `.png`.
* **--npy**: saves masks in `.npy` format as well.
* **--verbose**: displays detailed execution logs.
* **--basedir**: defines where results will be stored (default: `results`).
* **--index**: if multiple configurations exist in `config.json`, selects which one to run (use -1 for all). Most users do not need to modify this.

---

## 4. Running in Practice

With everything configured, simply run:

```bash
uv run CellViability --config config.json --instances --npy --verbose
```

If everything is correct, the system will:

* Read images inside each plate folder, such as `screen/P1`, `screen/P2`, etc.
* Apply the parameters defined in `config.json`.
* Generate masks and intermediate files.
* Save and organize results in the specified directory.

---

## 5. Next Steps

* Validate the results inside the `results/` folder.
* Adjust the `config.json` when needed.
* Repeat the analysis with new parameters as necessary.

---

## 6. Expected Outputs

* A **summary CSV** containing nucleus counts, INCPe, and identifiers for screen, plate, and well.
* A **morphology CSV** containing all morphological measurements (e.g., eccentricity, area, size).
* A **hits CSV** listing candidate hits based on Z-score and INCPe.
* Two **heatmaps per plate**: one for nucleus count and one for INCPe, both with control-location markings.
* **.png files containing the overlay of the segmentation mask on the original image**, generated for each individual image located in `screen/P1`, `screen/P2`,
