# Configuration file: `config.json`

The `config.json` file defines all parameters required by **CellViability** to run an analysis, including plate layout, control wells, filtering thresholds, preprocessing settings, and data paths. This configuration ensures reproducibility and allows the protocol to be adapted to different experimental designs.

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
    "filter": {
      "Z": 0.5,
      "inCPE": 0.3
    },
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

## JSON fields

| Field | Description |
| --- | --- |
| **`controls`** | Well identifiers (e.g., "A01", "B01") for negative controls (uninfected, untreated) and positive controls (infected, untreated), used for normalization and quality control. |
| **`datadir`** | Root directory containing the image data for the screening experiment. |
| **`fields`** | Number of image fields acquired per well (typically 1). |
| **`filter`** | Quality and hit-selection thresholds: `Z` defines the minimum Z'-factor required for plate acceptance (default: 0.5), and `inCPE` defines the minimum inhibition of cytopathic effect for hit selection (default: 0.3). |
| **`parameters`** | Image preprocessing and segmentation settings, including fluorescence channel index, Gaussian smoothing parameter (`sigma`), acceptable nucleus size range (`min_size`, `max_size`, in pixels), and the aggregation method (`merge`) for multi-field data. |
| **`plates`** | List of plate identifiers included in the analysis. |
| **`wells`** | Total number of wells per plate. |
