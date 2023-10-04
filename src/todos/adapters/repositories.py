import abc
from datetime import datetime

from sqlalchemy import select

from todos.adapters import orm


class AbstractRepository(abc.ABC):
    pass


class TodoRepository(AbstractRepository):
    def __init__(self, session):
        self.session = session

    async def get(self, todo_id):
        query = select(orm.Todo).where(orm.Todo.id == todo_id)
        result = await self.session.execute(query)
        return result

    async def get_list(self):
        query = select(orm.Todo)
        result = await self.session.execute(query)
        return result.scalars().all()

    def create(self, data):
        query = orm.Todo(
            content=data.content,
            is_completed=False,
            order=data.order,
            created_at=datetime.now(),
            updated_at=datetime.now(),
        )
        self.session.add(query)
        self.session.commit()
        return query

    def update(self, todo_id, data):
        query = self.session.query(orm.Todo).filter(orm.Todo.id == todo_id).first()
        query.content = data.content
        query.is_completed = data.is_completed
        query.order = data.order
        query.updated_at = datetime.now()
        self.session.commit()
        return query
