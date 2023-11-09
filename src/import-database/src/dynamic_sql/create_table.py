from typing import Tuple


def create_table(table) -> Tuple[str, str]:
    drop = f"DROP TABLE IF EXISTS {table.name}"
    create = f"CREATE TABLE IF NOT EXISTS {table.name} ({table.column_datatype_string}, PRIMARY KEY ({table.primary_key}))"
    return drop, create
