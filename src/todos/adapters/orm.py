from litestar.contrib.sqlalchemy.base import BigIntBase
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, UniqueConstraint

from databases import ModelBase


class Todo(ModelBase):
    __tablename__ = "todo"

    id = Column(Integer, primary_key=True)
    content = Column(String(255))
    is_completed = Column(Integer)
    order = Column(Integer)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
