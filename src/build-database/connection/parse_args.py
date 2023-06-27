# =============================================================================
# SPSM Parse Configuration Info
# =============================================================================
#
# Function to parse configuration file
#
from typing import Tuple

import yaml


def parse_config(file: str) -> Tuple[dict, dict]:
    config = {
        "db_name": None,
        "db_user": None,
        "db_password": None,
        "db_port": None,
        "db_host": None,
    }
    with open(file, "r") as f:
        info = yaml.safe_load(f)
    config.update(info["connection"])
    return config, info
