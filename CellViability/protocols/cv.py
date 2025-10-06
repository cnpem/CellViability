# This source code is part of the BioIMA package and is distributed
# under the GNU GPL-3.0 license. Please see 'LICENSE' for
# further information.

"""
CellViability.protocols submodule to define protocols for cell viability analysis.
"""

__all__ = []

import pandas

from ..screening import Image, Screen


class CellViabilityProtocol:
    """
    A class to represent a cell viability analysis protocol.

    Attributes
    ----------
    config : dict
        A dictionary containing configuration for the protocol.
    name : str
        The name of the protocol.
    verbose : bool
        A flag to indicate whether to run in verbose mode.

    Methods
    -------
    _load_screening() -> Screening
        Loads and returns a Screening instance.
    execute()
        Executes the cell viability analysis protocol.
    """

    def __init__(self, config: dict, name: str, verbose: bool = False):
        self.config = config
        self.screen = self._load_screen(config, name)
        self.verbose = verbose

    def _load_screen(self, config: dict, name: str) -> Screen:
        """
        Loads and returns a Screen instance.

        Parameters
        ----------
        config : dict
            A dictionary containing configuration for the screen.
        name : str
            The name of the screen.

        Returns
        -------
        Screen
            An instance of the Screen class.
        """
        screen = Screen(config, name)
        return screen

    def _cell_counting(self, image) -> pandas.DataFrame:
        """
        Counts and characterizes cells in the given image.

        Parameters
        ----------
        image : Image
            The image to analyze.

        Returns
        -------
        pandas.DataFrame
            A DataFrame containing properties of the counted cells.
        """
        pass  # Implementation of the cell counting logic goes here

    def _preprocessing(self, image: Image) -> Image:
        """
        Preprocesses the images (e.g., filtering, normalization).

        Parameters
        ----------
        image : Image
            The image to preprocess.

        Returns
        -------
        Image
            The preprocessed image.
        """
        pass  # Implementation of the preprocessing logic goes here

    def _segmentation(self, image: Image) -> Image:
        """
        Segments the images to identify cells.

        Parameters
        ----------
        image : Image
            The image to segment.

        Returns
        -------
        Image
            The segmented image.
        """
        pass  # Implementation of the segmentation logic goes here

    def _zcore(self, counting: pandas.DataFrame) -> pandas.DataFrame:
        """
        Applies Z-score normalization to the cell counting results.

        Parameters
        ----------
        counting : pandas.DataFrame
            The DataFrame containing cell counting results.

        Returns
        -------
        pandas.DataFrame
            The normalized DataFrame.
        """
        pass  # Implementation of the Z-score normalization logic goes here

    def execute(self, merge: str = "sum") -> dict[str, pandas.DataFrame]:
        """
        Executes the cell viability analysis protocol.

        Parameters
        ----------
        merge : str, optional
            The method to merge fields, by default "sum". Options are "sum".

        Returns
        -------
        dict[str, pandas.DataFrame]
            A dictionary with plate names as keys and their corresponding
            analysis results as pandas DataFrames.
        """
        results = {}

        for plate in self.screen.plates:
            if self.verbose:
                print(f"> Analyzing plate {plate.name} ...")

            for well in plate.wells:
                if self.verbose:
                    print(f"{well.name}:", end=" ")

                for image in well.images:
                    if self.verbose:
                        print(f"{image.filename}", end=" ")
                    # Pre-processing
                    image = self._preprocessing(image)
                    # Segmentation
                    image = self._segmentation(image)
                    # Cell counting and characterization
                    counting = self._cell_counting(image)
                    # Calculate Z-score normalization
                    zcore = self._zcore(counting)
                    results[well.name] = zcore

                if self.verbose:
                    print("\n", end="", flush=True)

        return results
