from dataclasses import dataclass
from datetime import datetime

from pydantic import BaseModel


class Todo(BaseModel):
    id: int
    content: str
    is_completed: bool
    order: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class CreateTodo(BaseModel):
    content: str
    order: int


class UpdateTodo(BaseModel):
    content: str
    is_completed: bool
    order: int
