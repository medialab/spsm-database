# =============================================================================
# SPSM Base Classes and Methods for SQL Tables
# =============================================================================
#
# Base classes and methods for SQL columns and tables
#
from psycopg2.extensions import connection
from psycopg2 import OperationalError
from psycopg2.extensions import connection as psycopg2_connection
from utils import execute_query


# To help prevent spelling errors,
# constants of SQL data types
class DType:
    SERIAL = "SERIAL"
    INT = "INT"
    BIGINT = "BIGINT"
    TEXT = "TEXT"
    VAR20 = "VARCHAR(20)"
    VAR250 = "VARCHAR(250)"
    VAR600 = "VARCHAR(600)"
    PRIMARY = "PRIMARY KEY"
    NOTNULL = "NOT NULL"
    DATETIME = "TIMESTAMP"
    BOOL = "BOOLEAN"
    ARRAY = "TEXT[]"
    FLOAT = "FLOAT"


class BaseColumn(object):
    """Base class for an SQL table column object,
    possessing a method that converts its properties
    (column name, data type, etc.) into a string
    that can be used to create a table schema.
    """

    def __init__(self, name, dtype, *args) -> None:
        # Every column needs a name
        self.name = name
        # Every column needs a data type
        self.type = dtype
        # Set attributes for the column's other info
        self.other = ", ".join(args)

    def string(self) -> str:
        """Method to transform the column's details into a string."""
        fields = list(self.__dict__.values())
        return " ".join(fields)


class BaseTable:
    """Base class for an SQL table object, possessing basic class
    methods that are commonly used in the construction of a table.
    """

    def __init__(self) -> None:
        # An array of the table's columns
        self.columns: list[BaseColumn]
        # The name of the table
        self.name: str
        # The table's primary key
        self.pk: str

    def exists(self, connection: connection) -> bool:
        query = f"select exists(select * from information_schema.tables where table_name='{self.name}')"
        cursor = execute_query(connection=connection, query=query, return_cursor=True)
        if isinstance(cursor, list):
            return cursor[0][0]
        else:
            return False

    def create(
        self,
        force: bool = False,
        connection: connection | None = None,
    ) -> str | None:
        """Create an SQL table.

        Param:
        self (BaseTable): class attributes including:
                            - an array of BaseColumn objects
                            - the name of the table
                            - schema information
                            - the primary key column name
        force (bool): create whether or not the table exists
        connection (connection): PostgreSQL database connection
        """

        # Set the condition for the table's creation
        whether_table_exists = ""
        if not force:
            whether_table_exists = " IF NOT EXISTS"

        # Compose a string of each table's column schema details
        cols = ", ".join([c.string() for c in self.columns])

        # With the table's information, compose the CREATE TABLE query
        query = f"""
        CREATE TABLE{whether_table_exists} {self.name}({cols}, PRIMARY KEY({self.pk}));
        """

        # If a connection was given, immediately execute the query
        if connection:
            execute_query(connection=connection, query=query)
        # Otherwise, return composed query for some later use
        else:
            return query

    def drop(
        self, force: bool = False, connection: connection | None = None
    ) -> str | None:
        """Drop an SQL table.

        Param:
        self (BaseTable): class attributes including:
                            - the name of the table
        force (bool): drop whether or not the table exists
        connection (connection): PostgreSQL database connection
        """

        # Set the condition for the table's deletion
        if not force:
            condition = " IF EXISTS"
        else:
            condition = ""

        # Compose the DROP TABLE query
        query = f"""
        DROP TABLE{condition} {self.name} CASCADE;
        """

        # If a connection was given, immediately execute the query
        if connection:
            execute_query(connection=connection, query=query)
        # Otherwise, return composed query for some later use
        else:
            return query

    def insert_values(
        self,
        data: dict,
        connection: connection | None = None,
        on_conflict: str | None = None,
    ) -> str | None:
        """Create an SQL table.

        Param:
        self (BaseTable): class attributes including:
                            - an array of BaseColumn objects
                            - the name of the table
        data (dict): key-value pairs of column names and values
        connection (connection): PostgreSQL database connection

        Return:
        NA : if a connection was given, the SQL query is executed
             and nothing is returned
        query (str): if no connection was given, the query is returned
        """

        # Set up a protocol for when there is a conflict on the primary key
        conflict_condition = ""
        if on_conflict:
            conflict_condition = f" ON CONFLICT ({self.pk}) {on_conflict}"

        # Make values query parameter string
        values = data.values()
        query_parameters = ", ".join(["%s" for _ in values])

        # Compose the INSERT - VALUES command
        query = f"""
        INSERT INTO {self.name}({", ".join(data.keys())}) VALUES ({query_parameters}){conflict_condition};
        """

        # If a connection was given, immediately execute the query
        if connection:
            execute_query(connection=connection, query=query, values=tuple(values))
        # Otherwise, return composed query for some later use
        else:
            return query

    def add_foreign_key(
        self,
        foreign_key_column: str,
        target_table: str,
        target_table_primary_key: str,
        connection: connection | None = None,
    ):
        fk_name = f"{self.name}_{foreign_key_column}_{target_table}_{target_table_primary_key}"
        query = f"""
        ALTER TABLE {self.name} DROP CONSTRAINT IF EXISTS {fk_name};
        ALTER TABLE {self.name} ADD CONSTRAINT {fk_name}
        FOREIGN KEY({foreign_key_column}) REFERENCES {target_table}({target_table_primary_key})
        """
        if connection:
            execute_query(connection=connection, query=query)
        else:
            return query


def clear_table(connection: psycopg2_connection, table: BaseTable):
    table.create(connection=connection)
    table.drop(connection=connection)
    table.create(connection=connection)

    cursor = execute_query(
        connection=connection,
        query=f"""
SELECT column_name, data_type
FROM information_schema.columns
WHERE table_name = '{table.name}';
""",
        return_cursor=True,
    )
    if isinstance(cursor, list):
        schema = [f"{d[0]}({d[1].upper()})" for d in cursor]
        print(
            f"\nCreated table '{table.name}' with the following columns:\n{', '.join(schema)}"
        )


def basic_csv_row_cleaning(row: dict) -> dict:
    for k, v in row.items():
        if v == "":
            v = None
        elif isinstance(v, str):
            v = v.strip()
        row.update({k: v})
    return row
