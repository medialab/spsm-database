# =============================================================================
# SPSM Database Connection Init
# =============================================================================
#
# Init file to pass database connection and config to other functions

from connection.create_connection import connect
from connection.parse_args import parse_args

config, filepaths = parse_args()

connection = connect(config)
