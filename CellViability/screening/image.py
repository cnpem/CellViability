# This source code is part of the BioIMA package and is distributed
# under the GNU GPL-3.0 license. Please see 'LICENSE' for
# further information.

"""
CellViability.screening submodule to handle screening data.
"""

__all__ = ["Image"]

import os

import numpy
from bioio import BioImage


class Image:
    """This class is used for an image of a well.

    Attributes
    ----------
    _image : BioImage | None
        The BioImage object representing the image.
    filename : str | None
        The path to the image file.
    image : BioImage
        The BioImage object representing the image.
    """

    def __init__(self) -> None:
        """
        Initialize the Image object.
        """
        self.field: int | None = None
        self.filename: str | None = None
        self._image: BioImage | None = None

    def __str__(self) -> str:
        return f"<CellViability.screening.image.Image `{self.filename}` object at {hex(id(self))}>"

    def __repr__(self) -> str:
        return f"<CellViability.screening.image.Image `{self.filename}` object at {hex(id(self))}>"

    def lazyload(self, field: int, filename: str) -> "Image":
        """
        Lazily load image metadata (field and filename) without loading the image data.

        Parameters
        ----------
        field : int
            The field number (must be positive).
        filename : str
            Path to the image file.

        Raises
        ------
        FileNotFoundError
            If the image file is not found.
        ValueError
            If the field number is not positive.
        ValueError
            If the filename is not a valid string.
        """
        if not isinstance(field, int) or field < 1:
            raise ValueError("Field number must be a positive integer.")
        if not isinstance(filename, str) or not filename:
            raise ValueError("Filename must be a non-empty string.")
        if not os.path.exists(filename):
            raise FileNotFoundError(f"Image '{filename}' not found.")

        self.field = field
        self.filename = filename
        self._image = None

        return self

    def upload(self, image: BioImage) -> None:
        """
        Upload an image to this object.

        Parameters
        ----------
        image : BioImage
            The image to be saved.
        """
        self._image = image
        self.field = None
        self.filename = None

    @property
    def data(self) -> numpy.ndarray:
        """Return the image data as a numpy array.

        Returns
        -------
        numpy.ndarray
            The image data as a numpy array.
        """
        if self._image is None:
            if self.filename is None:
                raise ValueError("No image loaded or filename provided.")
            self._image = BioImage(self.filename)
        return self._image.data

    @property
    def image(self) -> BioImage:
        """Return the BioImage object.

        Returns
        -------
        BioImage
            The BioImage object representing the image.
        """
        if self._image is None:
            if self.filename is None:
                raise ValueError("No image loaded or filename provided.")
            self._image = BioImage(self.filename)
        return self._image
