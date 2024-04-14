from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, declared_attr
from sqlalchemy import text, Numeric
from datetime import datetime
from typing import Annotated
from sqlalchemy.orm import registry
from decimal import Decimal


created_at = Annotated[datetime, mapped_column(server_default=text("TIMEZONE('utc', now())"))]
int_def0 = Annotated[int, mapped_column(default=0, server_default="0")]
def_false = Annotated[bool, mapped_column(default=False, server_default="False")]
num_20_2 = Annotated[Decimal, 20]


class Base(DeclarativeBase):
    __abstract__ = True
    registry = registry(
        type_annotation_map={
            num_20_2: Numeric(20, 2),
        }
    )
    id: Mapped[int] = mapped_column(primary_key=True)

    @declared_attr
    def __tablename__(self) -> str:
        """
        Changes the table name from "CamelCase" to "camel_cases"
        :return:
        """
        table_name = str()
        for char in self.__name__:
            if char.isupper():
                if table_name:
                    table_name += "_"
                char = char.lower()
            table_name += char
        return f"{table_name}s"
