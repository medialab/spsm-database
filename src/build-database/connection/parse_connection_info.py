from argparse import ArgumentParser

import yaml


def parse_args() -> dict:
    parser = ArgumentParser()
    parser.add_argument("--db-name", required=False, help="name of the database (spsm)")
    parser.add_argument("--db-user", required=False, help="user's name")
    parser.add_argument("--db-password", required=False, help="user's password")
    parser.add_argument(
        "--db-port", required=False, help="port to connect to running server (5432)"
    )
    parser.add_argument(
        "--db-host", required=False, help="host used to connect to running server"
    )
    parser.add_argument(
        "--connection-file",
        required=False,
        help="a YAML file containing all the necessary connection information",
    )
    args = parser.parse_args()

    config = {
        "db_name": None,
        "db_user": None,
        "db_password": None,
        "db_port": None,
        "db_host": None,
    }

    if args.connection_file:
        with open(args.connection_file, "r") as f:
            info = yaml.safe_load(f)
            config.update(info)
    else:
        config = {
            "db_name": args.db_name,
            "db_user": args.db_user,
            "db_password": args.db_password,
            "db_port": args.db_port,
            "db_host": args.db_host,
        }

    return config
