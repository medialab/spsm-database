import psycopg2
import psycopg2.extensions
from connection.parse_connection_info import parse_args
from psycopg2 import OperationalError


def connect() -> psycopg2.extensions.connection | None:
    args = parse_args()
    connection = None
    try:
        connection = psycopg2.connect(
            database=args["db_name"],
            user=args["db_user"],
            password=args["db_password"],
            host=args["db_host"],
            port=args["db_port"],
        )
        print("Connection to PostgreSQL DB successful.")
    except OperationalError as e:
        print(f"The error {e} occured.")
    return connection
