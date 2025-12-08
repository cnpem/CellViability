import os
import time

import numpy
import pandas
import skimage.morphology
from bioio import BioImage
from csbdeep.utils import normalize
from matplotlib import pyplot as plt
from stardist import models
from stardist.plot import render_label

from CellViability import Image, Screen, load_config


def memory_usage():
    import pynvml

    pynvml.nvmlInit()
    handle = pynvml.nvmlDeviceGetHandleByIndex(0)
    info = pynvml.nvmlDeviceGetMemoryInfo(handle)
    used = info.used
    pynvml.nvmlShutdown()
    return used


def segment(config: str = "tests/benchmark/config.json", basedir: str = "tests/benchmark") -> dict[str, int]:
    """
    Run cell viability analysis based on a configuration file.

    Parameters
    ----------
    config : str
        Path to the configuration file (default is 'tests/benchmark/config.json').
    basedir : str
        Base directory for saving results (default is 'tests/benchmark').

    Returns
    -------
    dict[str, int]
        A dictionary mapping well names to cell counts.
    """
    # Get base directory
    basedir = os.path.join(basedir, "stardist")
    os.makedirs(basedir, exist_ok=True)

    # Load configuration
    configs = load_config(config)
    condition = next(iter(configs.keys()))

    # Load screen
    screen = Screen(configs[condition], condition)

    # Load the Cellpose model: cyto
    model = models.StarDist2D.from_pretrained("2D_versatile_fluo")

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
                masks, _ = model.predict_instances(normalize(image.data[0, channel, 0, :, :]))

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
    basedir = "tests/benchmark"

    # Replicates
    N = 10

    # Run segmentation using StarDist
    for i in range(N):
        start_time = time.perf_counter()
        cellcount = segment(config="tests/benchmark/config.json", basedir=basedir)
        elapsed = time.perf_counter() - start_time
        print(f"[{i}][ Elapsed time: {elapsed:.0f}s ]")

        # Save cell count to a file
        if i == 0:
            df = pandas.DataFrame.from_dict(cellcount, orient="index", columns=["cellcount"])
            df.to_csv(os.path.join(basedir, "stardist.csv"))

        # Save elapsed time to a file
        with open(os.path.join(basedir, "runtime.csv"), "a+") as f:
            f.write(f"StarDist,{i + 1},{elapsed:.2f}\n")
