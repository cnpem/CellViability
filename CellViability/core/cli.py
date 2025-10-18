# This source code is part of the BioIMA package and is distributed
# under the GNU GPL-3.0 license. Please see 'LICENSE' for
# further information.

import argparse

from ..protocols import CellViabilityProtocol
from .io import load_config


def cli() -> argparse.Namespace:
    """
    Command-line interface for running packing simulations based on a configuration file.

    Returns
    -------
    argparse.Namespace
        Parsed command-line arguments. Attributes include:
        - config (dict): Loaded configuration data from the specified file.
        - verbose (bool): Whether to print detailed information during execution.

    Notes
    -----
    The configuration file must be in JSON format and may contain multiple
    configuration entries corresponding to different experimental conditions.

    Example
    -------
    Run with a configuration file:
        CellViability --config config.json

    Enable verbose mode:
        CellViability --config config.json --verbose

    If no arguments are provided, the program displays this help message.

    Example configuration file
    --------------------------
    {
        "Condition1": {
            "datadir": "data/Condition1",
            "plates": ["P1", "P2", "P3"],
            "positive_control_columns": ["1", "24"],
            "negative_control_columns": ["2", "23"],
            "wells": 384,
            "fields": 1
        },
        "Condition2": {
            "datadir": "data/Condition2",
            "plates": ["P1", "P2", "P3"],
            "positive_control_columns": ["1", "24"],
            "negative_control_columns": ["2", "23"],
            "wells": 384,
            "fields": 1
        }
    }
    """
    parser = argparse.ArgumentParser(description="Run cell viability analysis based on a configuration file.")
    parser.add_argument("--config", required=True, type=str, help="Path to the configuration file.")
    parser.add_argument(
        "--index",
        type=int,
        default=-1,
        help="Index (0-based) of the configuration to run. Use -1 to run all configurations. Default is -1.",
    )
    parser.add_argument(
        "--npy",
        action="store_true",
        help="If set, saves instance segmentation masks as .npy files.",
        default=False,
    )
    parser.add_argument(
        "--instances",
        action="store_true",
        help="If set, saves instance segmentation masks as .png files.",
        default=True,
    )
    parser.add_argument(
        "--basedir",
        type=str,
        default="results",
        help="Base directory for saving results. Default is 'results'.",
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Print detailed information about the selected configuration.",
    )

    # Parse arguments
    args = parser.parse_args()

    # Load configuration
    args.config = load_config(args.config)

    return args


def run() -> None:
    # Parse command-line arguments
    args = cli()
    conditions = list(args.config.keys())

    # Select conditions to run
    if args.index < -1 or args.index >= len(conditions):
        raise ValueError(
            f"Index {args.index} is out of range. Must be between 0 and {len(conditions) - 1}, or -1 for all."
        )
    selected_conditions = conditions if args.index == -1 else [conditions[args.index]]

    # Run simulations
    for condition in selected_conditions:
        print(f"[==> Running condition: {condition}")
        if args.verbose:
            print(args.config[condition])
        cvp = CellViabilityProtocol(args.config[condition], condition, basedir=args.basedir, verbose=args.verbose)
        cvp.execute(npy=args.npy, instances=args.instances)
        print("[==> Done!\n")
