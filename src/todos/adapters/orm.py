from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, UniqueConstraint
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class Todo(Base):
    __tablename__ = "todo"

    id = Column(Integer, primary_key=True)
    content = Column(String(255))
    is_completed = Column(Integer)
    order = Column(Integer)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
