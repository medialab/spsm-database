# =============================================================================
# SPSM Parse Configuration Info
# =============================================================================
#
# Function to parse CLI argument and configuration file
#
from argparse import ArgumentParser
from typing import Tuple

import yaml


def parse_args() -> Tuple[dict, dict]:
    parser = ArgumentParser()
    parser.add_argument(
        "--config",
        required=True,
        help="a YAML file containing all the necessary connection information and the data file paths",
    )
    args = parser.parse_args()

    config = {
        "db_name": None,
        "db_user": None,
        "db_password": None,
        "db_port": None,
        "db_host": None,
    }

    with open(args.config, "r") as f:
        info = yaml.safe_load(f)
        config.update(info["connection"])
        filepaths = info["data file absolute paths"]

    return config, filepaths
