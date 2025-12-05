import os
import time

import numpy
import pandas
import skimage.morphology
from bioio import BioImage
from cellpose import models
from matplotlib import pyplot as plt
from stardist.plot import render_label

from CellViability import Image, Screen, load_config


def segment(
    config: str = "tests/experiments/config.json", basedir: str = "tests/experiments/results"
) -> dict[str, int]:
    """
    Run cell viability analysis based on a configuration file using Cellpose 4.

    Parameters
    ----------
    config : str
        Path to the configuration file (default is 'tests/experiments/config.json').
    basedir : str
        Base directory for saving results.

    Returns
    -------
    dict[str, int]
        A dictionary mapping well names to cell counts.
    """
    # Get base directory
    basedir = os.path.join(basedir, "cellpose4")
    os.makedirs(basedir, exist_ok=True)

    # Load configuration
    configs = load_config(config)
    condition = next(iter(configs.keys()))

    # Load screen
    screen = Screen(configs[condition], condition)

    # Load the Cellpose model: cpsam
    model = models.Cellpose(model_type="cpsam", gpu=True)

    # Get parameters from config
    channel = configs[condition]["parameters"].get("channel", 0)
    min_size = configs[condition]["parameters"].get("min_size", 0)
    max_size = configs[condition]["parameters"].get("max_size", 500)

    # Run segmentation for all images in the screen
    cellcount = {}
    for plate in screen.plates:
        basedir = os.path.join(basedir, screen.name, plate.name)
        os.makedirs(basedir, exist_ok=True)
        for well in plate.wells:
            for image in well.images:
                outfile = os.path.join(basedir, os.path.basename(image.filename))

                # Segment image
                masks, _, _ = model.eval(
                    image.data[0, channel, 0, :, :],
                    diameter=None,
                    min_size=min_size,
                    channels=[0, 0],
                )

                if min_size > 0:
                    masks = skimage.morphology.remove_small_objects(masks, min_size=int(min_size))

                if max_size < 1e6:
                    masks = masks ^ skimage.morphology.remove_small_objects(masks, min_size=int(max_size))

                # Return the segmented image
                segmented = Image()
                segmented.upload(BioImage(masks))

                # Save mask
                plt.figure()
                plt.imshow(render_label(segmented.data[0, 0, 0, :, :], img=image.data[0, 0, channel, :, :]))
                plt.axis("off")
                plt.savefig(outfile, bbox_inches="tight", pad_inches=0)
                plt.close()

                # Save cellcount
                # NOTE: Subtract 1 for background
                cellcount[well.name] = len(numpy.unique(masks)) - 1

    return cellcount


if __name__ == "__main__":
    # Set base directory for results
    basedir = "tests/experiments/results"

    # Run segmentation using StarDist
    start_time = time.perf_counter()
    cellcount = segment(config="tests/experiments/config.json", basedir=basedir)
    elapsed = time.perf_counter() - start_time
    print(f"[ Elapsed time: {elapsed:.0f}s ]")

    # Save cell count to a file
    df = pandas.DataFrame.from_dict(cellcount, orient="index", columns=["cellcount"])
    df.to_csv(os.path.join(basedir, "cellpose4.csv"))

    # Save elapsed time to a file
    with open(os.path.join(basedir, "runtime.csv"), "a+") as f:
        f.write(f"Cellpose4,{elapsed:.2f}\n")
