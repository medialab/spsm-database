import psycopg2
import psycopg2.extensions
from psycopg2 import OperationalError


def connect(config: dict) -> psycopg2.extensions.connection | None:
    connection = None
    try:
        connection = psycopg2.connect(
            database=config["db_name"],
            user=config["db_user"],
            password=config["db_password"],
            host=config["db_host"],
            port=config["db_port"],
        )
        print("Connection to PostgreSQL DB successful.")
    except OperationalError as e:
        print(f"The error {e} occured.")
    return connection
