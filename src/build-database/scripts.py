# Forge scripts for SQL queries


def create_table_statement(table_name: str, columns: list) -> str:
    return f"CREATE TABLE IF NOT EXISTS {table_name}({column_string(columns)});"


def drop_table_statement(table_name: str) -> str:
    return f"DROP TABLE IF EXISTS {table_name}"


def column_string(columns: list) -> str:
    s = ", ".join(columns)
    return f"({s})"


def value_string(values: list) -> str:
    return ", ".join(values)


def insert_values_statement(table_name: str, values: list, columns: list | None = None):
    if columns:
        c = column_string(columns)
    else:
        c = ""
    return f"INSERT INTO {table_name}{c} VALUES ({value_string(values)})"
