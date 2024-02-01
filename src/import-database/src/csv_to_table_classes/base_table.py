import ast
from abc import ABC, abstractmethod
from datetime import datetime
from importlib.resources import files
from typing import Dict, List

import yaml
from psycopg2.extensions import connection as Connection

import tables
from connection import execute_query


class TableBase(ABC):
    def __init__(self, yaml_stem: str) -> None:
        info = self.from_yaml(yaml_stem)
        self.name = info["name"]
        self.primary_key = info["primary_key"]
        self.column_names = info["column_names"]
        self.column_dtypes = info["column_dtypes"]
        self.column_dtypes_string = info["column_dtypes_string"]
        self.bool_columns = info["bool_columns"]
        self.array_columns = info["array_columns"]

    def from_yaml(self, yaml_stem: str) -> Dict:
        with open(files(tables).joinpath(yaml_stem)) as f:  # type:ignore
            info = yaml.safe_load(f)
        column_datatypes = {}
        for d in info["columns"]:
            column_datatypes.update(d)
        return {
            "name": info["name"],
            "primary_key": info["primary_key"],
            "column_names": list(column_datatypes.keys()),
            "column_dtypes": column_datatypes,
            "column_dtypes_string": ", ".join(
                [f"{k} {v}" for k, v in column_datatypes.items()]
            ),
            "bool_columns": [k for k, v in column_datatypes.items() if v == "BOOLEAN"],
            "array_columns": [k for k, v in column_datatypes.items() if v == "TEXT[]"],
        }

    def _create_table(self, connection: Connection, reset: bool) -> None:
        create = f"CREATE TABLE IF NOT EXISTS {self.name} ({self.column_dtypes_string}, PRIMARY KEY ({self.primary_key}))"
        if reset:
            drop = f"DROP TABLE IF EXISTS {self.name}"
            execute_query(connection=connection, query=drop)
        execute_query(connection=connection, query=create)
        print(f"\nCreated table '{self.name}'.")

    def _compose_on_conflict(self):
        updated_columns = [
            col for col in self.column_names if col not in self.primary_key.split(",")
        ]
        excluded_columns = [f"EXCLUDED.{col}" for col in updated_columns]
        return f"""
        ON CONFLICT ({self.primary_key}) DO UPDATE
        SET ({", ".join(updated_columns)}) = ({", ".join(excluded_columns)})
        """

    def _insert(self, connection: Connection, clean_row: Dict, conflict: str) -> None:
        columns = ", ".join(clean_row.keys())
        values = clean_row.values()
        query_parameters = ", ".join(["%s" for _ in values])
        query = f"""
        INSERT INTO {self.name}({columns}) VALUES ({query_parameters}){conflict}
        """
        execute_query(connection=connection, query=query, values=tuple(values))

    def _clean_csv_row(self, row: Dict, prefix: str = "") -> Dict:
        clean_row = {}
        for file_column_name, v in row.items():
            # Adjust column name in relation to table column names if necessary
            table_column_name = file_column_name.replace(prefix, "")

            # If the column is not in the table, ignore it and its value
            if table_column_name not in self.column_names:
                continue

            # Remove white space and convert empty strings to None
            v = v.strip()
            if v == "":
                v = None

            # Remove null values
            if v:
                v = v.replace("\x00", "")

            # Cast booleans
            if v and table_column_name in self.bool_columns:
                v = bool(int(v))

            # Cast timestamps
            if v and "timestamp" in table_column_name:
                try:
                    v = str(datetime.fromtimestamp(int(v)))
                except TypeError as e:
                    pass

            # Cast arrays
            if isinstance(v, str) and table_column_name in self.array_columns:
                potential_array = v
                # If the data is written as a list (i.e. coordinates), read it literally
                if potential_array.startswith("[") and potential_array.endswith("]"):
                    try:
                        v = ast.literal_eval(potential_array)
                    except Exception:
                        pass
                    # Otherwise, try to unnest the data on the | delimiter
                else:
                    v = potential_array.split("|")

            clean_row.update({table_column_name: v})
        return clean_row
