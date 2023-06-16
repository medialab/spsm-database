from connection import connection
from queries import create_table, drop_table, insert


def main():
    if connection:
        drop_table(connection=connection, table_name="test")
        schema = [
            "id bigserial primary key",
            "fruit text NOT NULL",
            "color text NOT NULL",
        ]
        create_table(connection=connection, table_name="test", table_schema=schema)
        values = ["1", "apple", "red"]
        insert(connection=connection, table_name="test", values=values)


if __name__ == "__main__":
    main()
