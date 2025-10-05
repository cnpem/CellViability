# This source code is part of the BioIMA package and is distributed
# under the GNU GPL-3.0 license. Please see 'LICENSE' for
# further information.

"""
CellViability.screening submodule to handle screening data.
"""

__all__ = ["Image"]

import os

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

    def __init__(self):
        """
        Initialize the Image object.
        """
        self.filename: str | None = None
        self._image: BioImage | None = None

    def __str__(self):
        return f"<CellViability.screening.image.Image `{self.filename}` object at {hex(id(self))}>"

    def __repr__(self):
        return f"<CellViability.screening.image.Image `{self.filename}` object at {hex(id(self))}>"

    def lazyload(self, filename: str):
        """
        Load an image from filename.

        Parameters
        ----------
        filename : str
            Path to the image file.

        Raises
        ------
        FileNotFoundError
            If the image file is not found.
        """
        # Check if image exists
        if not os.path.exists(filename):
            raise FileNotFoundError(f"Image '{filename}' not found.")

        self.filename: str = filename

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
