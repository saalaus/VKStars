import sqlalchemy as sa
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import declarative_base


class BaseModel:
    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    def __repr__(self):
        model = self.__class__.__name__
        table:  sa.Table = sa.inspect(self.__class__)
        columns: list[sa.Column] = table.columns
        values = {
            column.name: getattr(self, column.name)
            for column in columns if getattr(self, column.name) is not None
        }
        value_str = " ".join(f"{name}={value!r}" for name, value in values.items())
        return f"<{model} {value_str}>"


BaseModel = declarative_base(cls=BaseModel)
