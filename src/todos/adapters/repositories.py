import abc
from datetime import datetime

from sqlalchemy import delete, insert, select, update

from todos.adapters import orm


class AbstractRepository(abc.ABC):
    pass


class TodoRepository(AbstractRepository):
    def __init__(self, session):
        self.session = session

    async def get(self, todo_id: int) -> orm.Todo:
        query = select(orm.Todo).where(orm.Todo.id == todo_id)
        result = await self.session.execute(query)
        return result.scalars().first()

    async def get_list(self) -> list[orm.Todo]:
        query = select(orm.Todo)
        result = await self.session.execute(query)
        return result.scalars().all()

    async def create(self, data: dict) -> orm.Todo:
        query = insert(orm.Todo).values(**data).returning(orm.Todo)
        result = await self.session.execute(query)
        return result.scalars().first()

    async def update(self, todo_id: int, data: dict) -> orm.Todo:
        query = (
            update(orm.Todo)
            .where(orm.Todo.id == todo_id)
            .values(**data)
            .returning(orm.Todo)
        )
        result = await self.session.execute(query)
        return result.scalars().first()

    async def delete(self, todo_id: int) -> bool:
        query = delete(orm.Todo).where(orm.Todo.id == todo_id)
        result = await self.session.execute(query)
        return result.rowcount == 1
