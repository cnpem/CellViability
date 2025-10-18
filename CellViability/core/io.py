# This source code is part of the BioIMA package and is distributed
# under the GNU GPL-3.0 license. Please see 'LICENSE' for
# further information.

import json
import os
from typing import Any

__all__ = ["load_config"]


def _get_metadata_from_filename(filename: str) -> tuple[str, int, int, str]:
    """
    Extracts metadata from a given filename.

    Parameters
    ----------
    filename : str
        The filename to extract metadata from.

    Returns
    -------
    tuple
        A tuple containing row, column, field and extra information.

    Notes
    -----
    The filename is expected to follow the Columbus 2.4.0.104236 build.
    Example filename: '001001-1-001001001.tif
    where:
        - '001001' is the well (row and column)
        - '1' is the field
        - '001001001' is extra information (e.g., timepoint, channel, z-stack)
    """
    basename: str = os.path.basename(filename)
    row: str = chr(64 + int(basename[0:3]))
    column: int = int(basename[3:6])
    field: int = int(basename[7:8])
    extra: str = basename[9:18]

    return row, column, field, extra


def load_config(filename: str = "config.json") -> dict:
    """
    Loads the configuration from a JSON file.

    Parameters
    ----------
    filename : str, optional
        The path to the configuration file, by default "config.json".

    Returns
    -------
    dict
        The configuration dictionary.
    """
    # Check if config file exists
    if not os.path.exists(filename):
        raise FileNotFoundError(f"Configuration file '{filename}' not found.")

    # Load and return the configuration
    with open(filename) as f:
        config: dict[str, Any] = json.load(f)

    return config
