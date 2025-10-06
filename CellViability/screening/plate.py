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
        self.name = name

        # Get data directory from the configuration
        if not os.path.exists(datadir):
            raise ValueError(f"Data directory '{datadir}' not found in the configuration.")
        self.datadir = datadir

        # Load wells
        self.wells: list[Well] = self._load_wells(config)

        # Check if number of wells matches expected number from config
        if len(self.wells) != config.get("wells"):
            raise ValueError(
                f"Number of wells in plate '{self.name}' ({len(self.wells)}) does not match expected number ({config.get('wells')})."
            )

    def __str__(self):
        return f"<CellViability.screening.plate.Plate `{self.name}` object at {hex(id(self))}>"

    def __repr__(self):
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
        wells = {}

        # Get files in datadir
        for filename in sorted(os.listdir(self.datadir)):
            if filename.endswith(".tif"):
                # Get metadata from filename
                # Columbus 2.4.0.104236 build format
                # Example: '001001-1-001001001.tif
                row, column, _, _ = _get_metadata_from_filename(filename)
                well = f"{row}{column:02d}"

                # Group images by well
                wells.setdefault(well, []).append(os.path.join(self.datadir, filename))

        # Sort wells by row and column
        sorted_wells = sorted(wells.keys(), key=well_sort)

        # Load wells in sorted order
        wells = [Well(config, wellname, wells[wellname]) for wellname in sorted_wells]

        return wells

    def well(self, wellname: str) -> Well:
        """Return a well object.

        Parameters
        ----------
        wellname : str
            The name of the well.

        Returns
        -------
        Well
            The well object.
        """
        # Check if well is loaded
        if len(self.wells) == 0:
            raise ValueError("Wells not loaded. Please load wells first.")

        # Check if well index is out of bounds
        if wellname not in [well.wellname for well in self.wells]:
            raise ValueError(f"Well {wellname} does not exist in plate.")

        # Get index of well in wells
        idx = [well.wellname for well in self.wells].index(wellname)

        return self.wells[idx]
