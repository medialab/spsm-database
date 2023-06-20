from psycopg2.extensions import connection
from queries import execute_query


class BaseColumn(object):
    def __init__(self, name, type, **kwargs) -> None:
        self.name = name
        self.type = type
        for k, v in kwargs.items():
            setattr(self, k, v)

    def string(self) -> str:
        fields = list(self.__dict__.values())
        return " ".join(fields)


class BaseTable:
    def __init__(self) -> None:
        self.columns: list[BaseColumn]
        self.name: str
        self.schema_addendum: list = []
        self.pk: str

    def column_schema(self) -> str:
        schema = []
        for column in self.columns:
            schema.append(column.string())
        return ", ".join(schema)

    def fields(self) -> dict:
        d = {}
        for column in self.columns:
            d.update({column.name: ""})
        return d

    def create(
        self,
        force: bool = False,
        connection: connection | None = None,
    ) -> str | None:
        condition = ""
        if not force:
            condition = " IF NOT EXISTS"
        if len(self.schema_addendum) > 0:
            schema_addendum = ", ".join([a for a in self.schema_addendum])
            schema_addendum = ", " + schema_addendum
        else:
            schema_addendum = ""
        query = f"""
        CREATE TABLE{condition} {self.name}({self.column_schema()}{schema_addendum});
        """
        if connection:
            execute_query(connection=connection, query=query)
        else:
            return query

    def drop(
        self, force: bool = False, connection: connection | None = None
    ) -> str | None:
        if not force:
            condition = " IF EXISTS"
        else:
            condition = ""
        query = f"""
        DROP TABLE{condition} {self.name} CASCADE;
        """
        if connection:
            execute_query(connection=connection, query=query)
        else:
            return query

    def insert_values(
        self,
        data: dict,
        connection: connection | None = None,
        on_conflict: str | None = None,
    ) -> str | None:
        # Set up protocol for when there is a conflict on the primary key
        c = ""
        if on_conflict:
            c = f" ON CONFLICT ({self.pk}) {on_conflict}"
        # Cast the values as strings, wrapped in single quotes
        values, columns = [], []
        for column_name, value in data.items():
            if value:
                columns.append(column_name)
                values.append(f"'{value}'")
        # Create insert command
        query = f"""
        INSERT INTO {self.name}({", ".join(columns)}) VALUES ({", ".join(values)}){c};
        """
        if connection:
            execute_query(connection=connection, query=query)
        else:
            return query
