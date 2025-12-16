# This source code is part of the BioIMA package and is distributed
# under the GNU GPL-3.0 license. Please see 'LICENSE' for
# further information.

"""
CellViability.protocols submodule to define protocols for cell viability analysis.
"""

__all__ = ["CellViabilityProtocol"]

import os

import matplotlib.pyplot as plt
import numpy
import pandas
import skimage.filters
import skimage.measure
import stardist.models
from bioio import BioImage
from csbdeep.utils import normalize
from stardist.plot import render_label

from ..core.visualization import plate_map
from ..screening import Image, Plate, Screen, Well


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

    def __init__(self, config: dict, name: str, basedir: str = "results", verbose: bool = False) -> None:
        self.config: dict = config
        self.screen: Screen = self._load_screen(config, name)
        self.model: stardist.models.model2d.StarDist2D | None = None
        self.basedir: str = basedir
        self.verbose: bool = verbose

    # -------------------------------------------------------------------------
    # Loading and setup
    # -------------------------------------------------------------------------
    def _create_directories(self, plate: Plate, npy: bool = False, instances: bool = False) -> None:
        """
        Creates necessary directories for storing results.

        Parameters
        ----------
        plate : str
            The name of the plate.
        npy : bool, optional
            If True, creates a directory for .npy files, by default False.
        instances : bool, optional
            If True, creates a directory for instance segmentation masks, by default False.
        """
        platedir = os.path.join(self.basedir, self.screen.name, plate.name)
        os.makedirs(platedir, exist_ok=True)

        if instances:
            os.makedirs(os.path.join(platedir, "instances"), exist_ok=True)
        if npy:
            os.makedirs(os.path.join(platedir, "npy"), exist_ok=True)

    def _load_model(self, warmup: bool = True) -> stardist.models.model2d.StarDist2D:
        """
        Loads the pre-trained StarDist2D model for cell segmentation.

        Parameters
        ----------
        use_gpu : bool, optional
            Whether to use GPU for model inference, by default True.

        Returns
        -------
        StarDist2D
            The loaded StarDist2D model.
        """
        model: stardist.models.model2d.StarDist2D = stardist.models.StarDist2D.from_pretrained("2D_versatile_fluo")

        # Warm-up the model (optional, but can speed up first prediction)
        if warmup:
            for _ in range(10):
                _ = model.predict_instances(numpy.zeros((256, 256), dtype=numpy.float32))

        return model

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
        return Screen(config, name)

    # -------------------------------------------------------------------------
    # Image processing and characterization
    # -------------------------------------------------------------------------
    def _segment(
        self,
        image: Image,
        channel: int = 0,
        sigma: float = 1.0,
        min_size: int = 0,
        max_size: int = 1000000,
    ) -> Image:
        """
        Segments the images to identify cells.

        Parameters
        ----------
        image : Image
            The image to segment.
        channel : int, optional
            The channel to process, by default 0.
        sigma : float, optional
            The standard deviation for Gaussian filtering, by default 1.0.
        min_size : int, optional
            The minimum object size (in pixels) to keep, by default 0.
        max_size : int, optional
            The maximum object size (in pixels) to keep, by default 1e6.

        Returns
        -------
        Image
            The segmented image.
        """
        img: numpy.ndarray = image.data[0, 0, channel, :, :]

        # Gaussian smoothing and normalization
        filtered: numpy.ndarray = skimage.filters.gaussian(img, sigma=sigma)

        # Instance segmentation using StarDist
        if self.model is not None:
            labels: numpy.ndarray
            labels, _ = self.model.predict_instances(normalize(filtered))

        if min_size > 0:
            labels = skimage.morphology.remove_small_objects(labels, min_size=int(min_size))

        if max_size < 1e6:
            labels = labels ^ skimage.morphology.remove_small_objects(labels, min_size=int(max_size))

        # Return the segmented image
        segmented = Image()
        segmented.upload(BioImage(labels))

        return segmented

    def _characterize(self, segmented: Image) -> pandas.DataFrame:
        """
        Counts and characterizes cells in the given image.

        Parameters
        ----------
        segmented : Image
            The segmented image to analyze.

        Returns
        -------
        pandas.DataFrame
            A DataFrame containing properties of the counted cells.
        """
        props = skimage.measure.regionprops_table(
            segmented.data[0, 0, 0, :, :],
            properties=[
                "label",
                "area",
                "perimeter",
                "eccentricity",
            ],
        )

        return pandas.DataFrame(props)

    def _analyze_well(self, plate: Plate, well: Well, parameters: dict, npy: bool, instances: bool) -> tuple:
        """
        Analyzes a single well in a plate.

        Parameters
        ----------
        plate : Plate
            The plate containing the well.
        well : Well
            The well to analyze.
        parameters : dict
            A dictionary containing analysis parameters.
        npy : bool
            If True, saves instance segmentation masks as .npy files.
        instances : bool
            If True, saves instance segmentation masks as .png files.

        Returns
        -------
        tuple
            A tuple containing the number of cells and their properties.
        """
        # Characterizations to be calculated
        ncells: int = 0
        properties: list[pandas.DataFrame] = []

        n = [] * len(well.images)
        for image in well.images:
            if self.verbose:
                print(f"{image.filename}", end=" ")

            # Pre-processing and Segmentation
            segmented: Image = self._segment(
                image,
                channel=parameters.get("channel", 0),
                sigma=parameters.get("sigma", 1.0),
                min_size=parameters.get("min_size", 0.0),
                max_size=parameters.get("max_size", 1e6),
            )

            # Basename for saving files
            if instances or npy:
                basename: str = os.path.splitext(os.path.basename(image.filename))[0]
            platedir = os.path.join(self.basedir, self.screen.name, plate.name)

            # Save .png file
            if instances:
                filename: str = os.path.join(platedir, "instances", f"{basename}.tiff")
                self._save_instances(image, segmented, filename)

            # Save .npy file
            if npy:
                filename = os.path.join(platedir, "npy", f"{basename}.npy")
                self._save_npy(segmented, filename)

            # Cell properties characterization
            props: pandas.DataFrame = self._characterize(segmented)
            props["screen"] = self.screen.name
            props["plate"] = plate.name
            props["well"] = well.name
            props["field"] = image.field
            properties.append(props)

            # Cell counting
            n.append(int(props["label"].count()))

        # Merge fields
        if parameters.get("merge", "sum") == "sum":
            ncells = sum(n)

        return ncells, pandas.concat(properties, ignore_index=True)

    def _analyze_plate(
        self, plate: Plate, parameters: dict, npy: bool, instances: bool
    ) -> tuple[pandas.DataFrame, pandas.DataFrame]:
        """
        Analyzes a single plate in the screening.

        Parameters
        ----------
        plate : Plate
            The plate to analyze.
        parameters : dict
            A dictionary containing analysis parameters.
        npy : bool
            If True, saves instance segmentation masks as .npy files.
        instances : bool
            If True, saves instance segmentation masks as .png files.

        Returns
        -------
        tuple[pandas.DataFrame, pandas.DataFrame]
            A tuple containing the number of cells and their properties.
        """
        # Characterizations to be calculated
        ncells: dict[str, int] = {}
        properties: list[pandas.DataFrame] = []

        for well in plate.wells:
            if self.verbose:
                print(f"> Analyzing well {well.name} ...")

            # Analyze the well
            ncells[well.name], props = self._analyze_well(plate, well, parameters, npy, instances)
            properties.append(props)

            if self.verbose:
                print("\n", end="", flush=True)

        # Convert cell counting to DataFrame
        df_ncells: pandas.DataFrame = (
            pandas.DataFrame.from_dict(ncells, orient="index", columns=["ncells"])
            .reset_index()
            .rename(columns={"index": "well"})
        )
        df_ncells.insert(0, "plate", plate.name)

        # Convert properties to DataFrame
        df_properties: pandas.DataFrame = pandas.concat(properties, ignore_index=True)

        return df_ncells, df_properties

    # -------------------------------------------------------------------------
    # Saving
    # -------------------------------------------------------------------------
    def _save_npy(self, image: Image, filename: str) -> None:
        """
        Saves the given image as a .npy file.

        Parameters
        ----------
        image : Image
            The image to save.
        filename : str
            The filename to save the .npy file.
        """
        numpy.save(filename, image.data)

    def _save_instances(self, image: Image, segmented: Image, filename: str) -> None:
        """
        Saves the instance segmentation mask as a .png file.

        Parameters
        ----------
        image : Image
            The original image.
        segmented : Image
            The segmented image to save.
        filename : str
            The filename to save the .png file.
        """
        # Get segmented channel
        channel = self.config["parameters"].get("channel", 0)

        plt.figure()
        plt.imshow(render_label(segmented.data[0, 0, 0, :, :], img=image.data[0, 0, channel, :, :]))
        plt.axis("off")
        plt.savefig(filename, bbox_inches="tight", pad_inches=0)
        plt.close()

    # -------------------------------------------------------------------------
    # Post-processing: Normalization (inCPE), Z-score and hit selecion
    # -------------------------------------------------------------------------
    def _zscore(self, ncells: pandas.DataFrame) -> float:
        """
        Applies Z-score normalization to the cell counting.

        Parameters
        ----------
        ncells : pandas.DataFrame
            The DataFrame containing cell counting.

        Returns
        -------
        float
            The Z-score value.

        Note
        ----
        Z-score formula: Z' = 1 - (3 * (sp + sn)) / |mp - mn|
        where sp and sn are the standard deviations of the positive and
        negative controls, and mp and mn are their means.
        """
        # Select positive and negative controls
        pos: pandas.Series = ncells.loc[ncells["well"].isin(self.config["controls"]["positive"]), "ncells"]
        neg: pandas.Series = ncells.loc[ncells["well"].isin(self.config["controls"]["negative"]), "ncells"]

        # Calculate Z-score for plate
        zscore: float = 1 - (3 * (pos.std() + neg.std())) / abs(pos.mean() - neg.mean())

        return zscore

    def _normalization(self, ncells: pandas.DataFrame) -> pandas.DataFrame:
        """
        Applies inCPE normalization to the cell counting.

        The inCPE (inhibition of cytopathic effect) is calculated as:

            inCPE = (Ncells - mean(Zpos)) / (mean(Zneg) - mean(Zpos))

        where:
            - Zpos: positive control wells (infected, untreated)
            - Zneg: negative control wells (non-infected, untreated)

        Parameters
        ----------
        ncells : pandas.DataFrame
            The DataFrame containing cell counts. Must include columns:
            'well' and 'ncells'.

        Returns
        -------
        pandas.DataFrame
            The DataFrame with an additional column 'inCPE'.
        """
        # Select positive and negative controls
        pos: pandas.Series = ncells.loc[ncells["well"].isin(self.config["controls"]["positive"]), "ncells"]
        neg: pandas.Series = ncells.loc[ncells["well"].isin(self.config["controls"]["negative"]), "ncells"]

        # Compute inCPE normalization
        ncells["inCPE"] = (ncells["ncells"] - pos.mean()) / (neg.mean() - pos.mean())

        return ncells

    def _filter_candidates(
        self,
        data: dict[str, pandas.DataFrame],
        zscore_per_plate: pandas.DataFrame,
        zscore: float = 0.5,
        incpe: float = 0.3,
    ) -> pandas.DataFrame:
        """
        Filters candidate hits based on Z-score and inCPE thresholds.

        Parameters
        ----------
        data : dict[str,pandas.DataFrame]
            The dictionary containing cell counting and inCPE values for each plate.
        zscore_per_plate : pandas.DataFrame
            The DataFrame containing Z-scores per plate.
        zscore : float, optional
            The Z-score threshold for hit selection, by default 0.5.
        incpe : float, optional
            The inCPE threshold for hit selection, by default 0.3.

        Returns
        -------
        pandas.DataFrame
            A DataFrame containing the filtered candidate hits.
        """
        # Get approved plates based on Z-score
        approved: list[str] = zscore_per_plate.loc[zscore_per_plate["zscore"] >= zscore, "plate"].tolist()

        # Filter hits based on inCPE and approved plates
        hits: pandas.DataFrame = pandas.DataFrame()
        for plate in approved:
            # Get all data from approved plate
            plate_data: pandas.DataFrame = data[plate]

            # Remove controls from data
            plate_data = plate_data.loc[
                ~plate_data["well"].isin(self.config["controls"]["negative"])
                & ~plate_data["well"].isin(self.config["controls"]["positive"])
            ]

            # Select hits based on incpe
            plate_hits = plate_data[plate_data["inCPE"] >= incpe]
            hits = pandas.concat([hits, plate_hits], ignore_index=True)

        # Print approval rate
        print(f"> Approved plates: {len(approved)} ({(len(approved) / len(data)) * 100:.2f}%)")

        # Print number of hits
        print(f"> Number of hits: {len(hits)}")

        return hits

    # -------------------------------------------------------------------------
    # Execution
    # -------------------------------------------------------------------------
    def execute(
        self, npy: bool = False, instances: bool = False
    ) -> tuple[pandas.DataFrame, pandas.DataFrame, dict[str, pandas.DataFrame], dict[str, pandas.DataFrame]]:
        """
        Executes the cell viability analysis protocol.

        Parameters
        ----------
        npy : bool, optional
            If True, saves instance segmentation masks as .npy files, by default False.
        instances : bool, optional
            If True, saves instance segmentation masks as .png files, by default False.

        Returns
        -------
        pandas.DataFrame
            A DataFrame containing the filtered candidate hits.
        pandas.DataFrame
            A DataFrame containing Z-scores for all plates.
        dict[str, pandas.DataFrame]
            A dictionary with plate names as keys and their corresponding
            analysis results as pandas DataFrames.
        dict[str, pandas.DataFrame]
            A dictionary with plate names as keys and their corresponding
            morphology properties as pandas DataFrames.

        Notes
        -----
        The method processes each plate in the screening, analyzes each well,
        and applies the specified cell viability analysis protocol.
        """
        # Load the model if not already loaded
        if self.model is None:
            print("> Loading StarDist model ...")
            self.model = self._load_model(warmup=True)

        # Initialize ncells and morphology dictionary
        ncells: dict[str, pandas.DataFrame] = {}
        morphology: dict[str, pandas.DataFrame] = {}
        zscore: dict[str, float] = {}

        # Iterate over plates, wells, and images
        for plate in self.screen.plates:
            if self.verbose:
                print(f"> Analyzing plate {plate.name} ...")

            # Create directories for the plate
            self._create_directories(plate=plate, instances=instances, npy=npy)

            # Analyze the plate
            ncells[plate.name], properties = self._analyze_plate(
                plate=plate, parameters=self.config["parameters"], npy=npy, instances=instances
            )
            morphology[plate.name] = properties

            # Analyze zcore for the plate
            zscore[plate.name] = self._zscore(ncells[plate.name])

            # Save status file
            with open(os.path.join(self.basedir, self.screen.name, plate.name, "status"), "w") as f:
                if zscore[plate.name] >= 0.5:
                    f.write("SUCCESS")
                else:
                    print(f"Warning: Z-score {zscore[plate.name]:.2f} is below the cutoff of 0.5.")
                    f.write("FAILED")

            # Normalization (inCPE)
            ncells[plate.name] = self._normalization(ncells[plate.name])

            # Plate map visualization
            plate_map(
                filename=os.path.join(self.basedir, self.screen.name, plate.name, "ncells.html"),
                data=ncells[plate.name],
                colname="ncells",
                controls=self.config["controls"],
            )
            plate_map(
                filename=os.path.join(self.basedir, self.screen.name, plate.name, "inCPE.html"),
                data=ncells[plate.name],
                colname="inCPE",
                controls=self.config["controls"],
            )

            # Save morphology as Excel file
            morphology[plate.name].to_csv(
                f"{self.basedir}/{self.screen.name}/{plate.name}/morphology.csv.gz", index=False, compression="gzip"
            )

        # Combine all z-scores into a DataFrame
        zscore_per_plate = pandas.DataFrame(list(zscore.items()), columns=["plate", "zscore"])

        # Filter hits
        hits: pandas.DataFrame = self._filter_candidates(
            ncells,
            zscore_per_plate,
            zscore=self.config["filter"].get("zscore", 0.5),
            incpe=self.config["filter"].get("zscore", 0.3),
        )

        # Save ncells as multi-sheet Excel file
        with pandas.ExcelWriter(f"{self.basedir}/{self.screen.name}/summary.xlsx", engine="openpyxl") as writer:
            zscore_per_plate.to_excel(writer, sheet_name="Z-score", index=False)
            for plate in self.screen.plates:
                ncells[plate.name].to_excel(writer, sheet_name=plate.name, index=False)

        # Save hits to Excel file
        with pandas.ExcelWriter(f"{self.basedir}/{self.screen.name}/hits.xlsx", engine="openpyxl") as writer:
            hits.to_excel(writer, sheet_name="Hits", index=False)

        # Unload model from memory
        self.model = None

        return hits, zscore_per_plate, ncells, morphology
