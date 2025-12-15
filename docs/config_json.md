# `config.json` — Structure and Parameter Description

Below is the general structure of the `config.json` file used by **CellViability**. This file defines analysis parameters, plate organization, control identification, and data paths.

Example:

```json
{
  "screen": {
    "controls": {
      "negative": [
        "A01", "B01", "C01", "D01", "E01", "F01", "G01", "H01",
        "I01", "J01", "K01", "L01", "M01", "N01", "O01", "P01",
        "A24", "B24", "C24", "D24", "E24", "F24", "G24", "H24",
        "I24", "J24", "K24", "L24", "M24", "N24", "O24", "P24"
      ],
      "positive": [
        "A02", "B02", "C02", "D02", "E02", "F02", "G02", "H02",
        "I02", "J02", "K02", "L02", "M02", "N02", "O02", "P02",
        "A23", "B23", "C23", "D23", "E23", "F23", "G23", "H23",
        "I23", "J23", "K23", "L23", "M23", "O23", "N23", "P23"
      ]
    },
    "datadir": "screen",
    "fields": 1,
    "parameters": {
      "channel": 0,
      "max_size": 500,
      "merge": "sum",
      "min_size": 0,
      "sigma": 1.0
    },
    "plates": [
      "P1",
      "P2"
    ],
    "wells": 64
  }
}
```

## General Structure

The file is organized into **main blocks**, where the screening name (`"screen"`) is the identifier of the analysis.

It defines:

* Positive and negative controls
* Data directory
* Segmentation parameters
* Number of fields per well
* Plate identifiers
* Total number of wells

---

### 1. `controls`

Defines the positions of controls used for metric calculations.

#### negative

List of wells used as negative controls.

#### positive

List of wells used as positive controls.

The naming follows the standard format: `"A01"`, `"B02"`, etc.

---

### 2. `datadir`

```json
"datadir": "screen"
```

Directory where exported images used for analysis are stored.

---

### 3. `fields`

```json
"fields": 1
```

Number of fields per well.

---

### 4. `parameters`

Controls the parameters used in nucleus segmentation.

| Parameter | Description                                      |
| --------- | ------------------------------------------------ |
| channel   | Image channel used for segmentation.             |
| max_size  | Maximum allowed size for segmented objects.      |
| min_size  | Minimum allowed size for segmented objects.      |
| merge     | Strategy for merging fields (`sum`, `mean`).     |
| sigma     | Sigma used in the Gaussian filter for smoothing. |

---

### 5. `plates`

```json
"plates": ["P1", "P2"]
```

List of plates included in the analysis. The names must match the folder names containing the images.

---

### 6. `wells`

```json
"wells": 64
```

Total number of filled wells in the 384-well plate.
