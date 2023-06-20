from connection.create_connection import connect
from connection.parse_args import parse_args

config, filepaths = parse_args()

connection = connect(config)
