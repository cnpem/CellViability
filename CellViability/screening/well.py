# This source code is part of the BioIMA package and is distributed
# under the GNU GPL-3.0 license. Please see 'LICENSE' for
# further information.

"""
CellViability.screening submodule to handle screening data.
"""

__all__ = ["Well"]

import re

from ..core.io import _get_metadata_from_filename
from .image import Image


def well_sort(well: str) -> tuple[str, int]:
    """Sort wells by row and column.

    Parameters
    ----------
    well : str
        The well name.

    Returns
    -------
    Tuple[str, int]
        A tuple containing the row (str) and column (int) of the well.

    Raises
    ------
    ValueError
        If the well name is invalid.
    """
    # Extract row and column from well name
    match: re.Match | None = re.match(r"([A-Z])(\d+)", well)

    # Sort alphabetically by row and numerically by column
    if match:
        row: str
        col: str
        row, col = match.groups()
    else:
        raise ValueError(f"Invalid well name: {well}")

    return (row, int(col))


class Well:
    """This class is used for a well in a plate.

    Attributes
    ----------
    images : list[Image]
        The list of images in the well.
    name : str
        The name of the well.
    """

    def __init__(self, config: dict, name: str, filenames: list[str]):
        """
        Initialize the Well object.

        Parameters
        ----------
        config : dict
            The configuration dictionary.
        name : str
            The name of the well.
        filenames : List[str]
            List of paths to the images in the well.

        Raises
        ------
        ValueError
            If the number of images does not match the expected number from config.
        """
        # Process well name
        self.name: str = name

        # Load images
        self.images: list[Image] = self._load_images(filenames)

        # Check if number of images matches expected number from config
        if len(self.images) != config.get("fields"):
            raise ValueError(
                f"Number of images in well '{self.name}' ({len(self.images)}) does not match expected number ({config.get('fields')})."
            )

    def __str__(self) -> str:
        return f"<CellViability.screening.well.Well `{self.name}` object at {hex(id(self))}>"

    def __repr__(self) -> str:
        return f"<CellViability.screening.well.Well `{self.name}` object at {hex(id(self))}>"

    def _load_images(self, filenames: list[str]) -> list[Image]:
        """
        Load images from the well configuration.

        Parameters
        ----------
        filenames : list[str]
            List of paths to the images in the well.

        Returns
        -------
        list[Image]
            The list of images in the well.
        """
        # Load images from the well configuration
        images = []
        for filename in sorted(filenames):
            # Get metadata from filename
            # Columbus 2.4.0.104236 build format
            # Example: '001001-1-001001001.tif
            _, _, field, _ = _get_metadata_from_filename(filename)

            # Sort images by field
            images.append((field, filename))

        # Sort images by field number
        images.sort(key=lambda x: x[0])

        return [Image().lazyload(field, filename) for field, filename in images]

    def image(self, field: int) -> Image:
        """Return an image object.

        Parameters
        ----------
        field : int
            The field number. Examples: 1, 2, 3, etc.

        Returns
        -------
        Image
            The image object.

        Raises
        ------
        ValueError
            If images are not loaded or field does not exist.

        """
        # Check if well is loaded
        if len(self.images) == 0:
            raise ValueError("Images not loaded. Please load images first.")

        # Check if well index is out of bounds
        if field not in [image.field for image in self.images]:
            raise ValueError(f"Field #{field} does not exist in plate.")

        # Get index of well in wells
        idx = [image.field for image in self.images].index(field)

        return self.images[idx]
