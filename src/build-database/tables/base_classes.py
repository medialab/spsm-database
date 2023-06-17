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
        self.columns = []
        self.name = ""

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

    def create(self, force: bool = False) -> str:
        if not force:
            condition = " IF NOT EXISTS"
        else:
            condition = ""
        query = f"""
        CREATE TABLE{condition} {self.name}({self.column_schema()});
        """
        return query

    def drop(self, force: bool = False) -> str:
        if not force:
            condition = " IF EXISTS"
        else:
            condition = ""
        query = f"""
        DROP TABLE{condition} {self.name};
        """
        return query

    def insert_values(self, data: dict) -> str:
        values = [f"'{v}'" for v in data.values()]
        query = f"""
        INSERT INTO {self.name}({', '.join(data.keys())}) VALUES ({', '.join(values)});
        """
        return query
