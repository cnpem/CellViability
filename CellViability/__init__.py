# This source code is part of the BioIMA package and is distributed
# under the GNU GPL-3.0 license. Please see 'LICENSE' for
# further information.

"""
CellViability: A package for analyzing cell viability data from HTS assays.
"""

__version__ = "0.1.0"
__all__ = ["CellViabilityProtocol", "Image", "Plate", "Screen", "Well", "load_config"]

import os

# Suppress TensorFlow warnings and logs
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"
os.environ["XLA_FLAGS"] = "--xla_gpu_enable_latency_hiding_scheduler=false"

from .core.io import load_config
from .protocols import CellViabilityProtocol
from .screening import Image, Plate, Screen, Well
