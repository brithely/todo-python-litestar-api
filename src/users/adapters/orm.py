from litestar.contrib.sqlalchemy.base import BigIntBase
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, UniqueConstraint

from databases import ModelBase


class User(ModelBase):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    email = Column(String(255))
    password = Column(String(255))
