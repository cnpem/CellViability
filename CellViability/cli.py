# This source code is part of the BioIMA package and is distributed
# under the GNU GPL-3.0 license. Please see 'LICENSE' for
# further information.

import argparse

from .io import load_config
from .screening import Screen


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
        "--verbose",
        action="store_true",
        help="Print detailed information about the selected configuration.",
    )

    # Parse arguments
    args = parser.parse_args()

    # Load configuration
    args.config = load_config(args.config)

    return args


def run():
    # Parse command-line arguments
    args = cli()
    conditions = list(args.config.keys())

    # Select conditions to run
    selected_conditions = conditions  # if args.all else [conditions[args.index]]

    # Run simulations
    for condition in selected_conditions:
        print(f"[==> Running condition: {condition}")
        if args.verbose:
            print(args.config[condition])
        screen = Screen(args.config[condition], condition)
        print(screen)
        print("> Done!\n")
