# This source code is part of the BioIMA package and is distributed
# under the GNU GPL-3.0 license. Please see 'LICENSE' for
# further information.

"""
CellViability.screening submodule to handle screening data.
"""

__all__ = ["Plate"]

import os

from ..core.io import _get_metadata_from_filename
from .well import Well, well_sort


class Plate:
    """This class is used for a plate in a screening experiment.

    Attributes
    ----------
    datadir : str
        The directory where the plate data is stored.
    name : str
        The name of the plate.
    wells : list of Well
        The list of wells in the plate.
    """

    def __init__(self, config: dict, name: str, datadir: str):
        """
        Initialize the Plate object.

        Parameters
        ----------
        config : dict
            The configuration dictionary.
        name : str
            The name of the plate.
        datadir : str
            Path to the directory containing plate images.

        Raises
        ------
        ValueError
            If the data directory is not found.
        ValueError
            If the number of wells does not match the expected number from config.
        """
        # Process plate name
        self.name: str = name

        # Get data directory from the configuration
        if not os.path.exists(datadir):
            raise ValueError(f"Data directory '{datadir}' not found in the configuration.")
        self.datadir: str = datadir

        # Load wells
        self.wells: list[Well] = self._load_wells(config)

        # Check if number of wells matches expected number from config
        if len(self.wells) != config.get("wells"):
            raise ValueError(
                f"Number of wells in plate '{self.name}' ({len(self.wells)}) does not match expected number ({config.get('wells')})."
            )

    def __str__(self) -> str:
        return f"<CellViability.screening.plate.Plate `{self.name}` object at {hex(id(self))}>"

    def __repr__(self) -> str:
        return f"<CellViability.screening.plate.Plate `{self.name}` object at {hex(id(self))}>"

    def _load_wells(self, config: dict) -> list[Well]:
        """
        Load wells from the plate configuration.

        Parameters
        ----------
        config : dict
            The configuration dictionary.

        Returns
        -------
        list[Well]
            The list of wells in the plate.
        """
        raw: dict[str, list[str]] = {}

        # Get files in datadir
        for filename in sorted(os.listdir(self.datadir)):
            if filename.endswith(".tif"):
                # Get metadata from filename
                # Columbus 2.4.0.104236 build format
                # Example: '001001-1-001001001.tif
                row, column, _, _ = _get_metadata_from_filename(filename)
                well: str = f"{row}{column:02d}"

                # Group images by well
                raw.setdefault(well, []).append(os.path.join(self.datadir, filename))

        # Sort wells by row and column
        sorted_wells: list[str] = sorted(raw.keys(), key=well_sort)

        # Load wells in sorted order
        wells: list[Well] = [Well(config, wellname, raw[wellname]) for wellname in sorted_wells]

        return wells

    def well(self, name: str) -> Well:
        """Return a well object.

        Parameters
        ----------
        name : str
            The name of the well. Examples: 'A01', 'B12', etc.

        Returns
        -------
        Well
            The well object.
        """
        # Check if well is loaded
        if len(self.wells) == 0:
            raise ValueError("Wells not loaded. Please load wells first.")

        # Check if well index is out of bounds
        if name not in [well.name for well in self.wells]:
            raise ValueError(f"Well {name} does not exist in plate.")

        # Get index of well in wells
        idx: int = [well.name for well in self.wells].index(name)

        return self.wells[idx]
