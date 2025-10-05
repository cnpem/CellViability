# This source code is part of the BioIMA package and is distributed
# under the GNU GPL-3.0 license. Please see 'LICENSE' for
# further information.

"""
CellViability.screening submodule to handle screening data.
"""

__all__ = ["Screen"]

import os

from .plate import Plate


class Screen:
    """This class is used for a screen .

    Attributes
    ----------
    datadir : str
        The directory where the screening data is stored.
    name : str
        The name of the screening.
    plates : list[Plate]
        The list of plates in the screening.
    """

    def __init__(self, config: dict, name: str):
        """
        Initialize the Screen object.

        Parameters
        ----------
        config : dict
            The configuration dictionary.
        name : str
            The name of the screening.

        Raises
        ------
        ValueError
            If the data directory is not found in the configuration.
        """
        # Get screen name
        self.name: str = name

        # Get data directory from the configuration
        if not os.path.exists(config.get("datadir")):
            raise ValueError(f"Data directory '{config.get('datadir')}' not found in the configuration.")
        self.datadir: str = config.get("datadir")

        # Load plates from the experiment configuration
        self.plates: list[Plate] = self._load_plates(config)

    def __str__(self):
        return f"<CellViability.screening.Screen `{self.name}` object at {hex(id(self))}>"

    def __repr__(self):
        return f"<CellViability.screening.Screen `{self.name}` object at {hex(id(self))}>"

    def _load_plates(self, config: dict) -> list[Plate]:
        """
        Load plates from the experiment configuration.

        Parameters
        ----------
        config : dict
            The configuration dictionary.

        Returns
        -------
        list[Plate]
            The list of plates in the screening.
        """
        plates = []

        for platename in config.get("plates"):
            # Get the data directory for the plate
            path = os.path.join(config.get("datadir"), platename)

            # Create a Plate object and add it to the list
            plates.append(Plate(config, platename, path))

        return plates

    def plate(self, idx: int | str) -> Plate:
        """
        Return a plate object from plates attributes.

        Parameters
        ----------
        idx : int | str
            Index or name of the plate in plates attributes.
        """
        # Check if plate index is out of bounds
        if isinstance(idx, int):
            if idx < 0 or idx >= len(self.plates):
                raise ValueError(f"Plate index '{idx}' out of bounds.")
            return self.plates[idx]
        elif isinstance(idx, str):
            for plate in self.plates:
                if plate.name == idx:
                    return plate
            raise ValueError(f"Plate name '{idx}' not found.")
