from connection import connection
from tables.schemas import TestTable
from queries import execute_query


def main():
    if connection:
        table = TestTable()
        query = table.drop()
        execute_query(connection=connection, query=query)
        query = table.create()
        execute_query(connection=connection, query=query)
        data = {"fruit": "apple", "color": "red"}
        query = table.insert_values(data)
        print(query)
        execute_query(connection=connection, query=query)


if __name__ == "__main__":
    main()
