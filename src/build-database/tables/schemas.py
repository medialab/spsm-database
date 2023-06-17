# SQL Tables as classes
from dataclasses import dataclass
from tables.base_classes import BaseTable, BaseColumn

SERIAL = "BIGSERIAL"
INT = "INT"
TEXT = "TEXT"
PRIMARY = "PRIMARY KEY"


@dataclass
class TestTable(BaseTable):
    name = "test"
    pid = BaseColumn(name="id", type=SERIAL, **{"primary_key": PRIMARY})
    fruit = BaseColumn(name="fruit", type=TEXT)
    color = BaseColumn(name="color", type=TEXT)
    columns = [pid, fruit, color]
