# =============================================================================
# SPSM Base Classes for SQL Table Objects
# =============================================================================
#
# Base classes for SQL column and SQL table
#
from psycopg2.extensions import connection
from connection.execute_query import execute_query


class BaseColumn(object):
    """Base class for an SQL table column object,
    possessing a method that converts its properties
    (column name, data type, etc.) into a string
    that can be used to create a table schema.
    """

    def __init__(self, name, type, **kwargs) -> None:
        self.name = name
        self.type = type
        for k, v in kwargs.items():
            setattr(self, k, v)

    def string(self) -> str:
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
        # Additional commands to be added to the table's creation
        self.schema_addendum: list = []
        # The table's primary key
        self.pk: str

    def column_schema(self) -> str:
        """Convert the array of columns into a string
        that can be used in the SQL query to create
        the table.
        """
        schema = []
        for column in self.columns:
            schema.append(column.string())
        return ", ".join(schema)

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
        condition = ""
        if not force:
            condition = " IF NOT EXISTS"

        # Parse any additional constraints on the schema
        if len(self.schema_addendum) > 0:
            schema_addendum = ", " + ", ".join([a for a in self.schema_addendum])
        else:
            schema_addendum = ""

        # Using the class method column_schema, convert the column data into a string
        # and compose the full CREATE TABLE query
        query = f"""
        CREATE TABLE{condition} {self.name}({self.column_schema()}{schema_addendum});
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
        conflict = ""
        if on_conflict:
            conflict = f" ON CONFLICT ({self.pk}) {on_conflict}"

        # Cast the values as strings, wrapped in single quotes
        values, columns = [], []
        for column_name, value in data.items():
            if value:
                columns.append(column_name)
                values.append(f"'{value}'")

        # Compose the INSERT - VALUES command
        query = f"""
        INSERT INTO {self.name}({", ".join(columns)}) VALUES ({", ".join(values)}){conflict};
        """

        # If a connection was given, immediately execute the query
        if connection:
            execute_query(connection=connection, query=query)
        # Otherwise, return composed query for some later use
        else:
            return query
