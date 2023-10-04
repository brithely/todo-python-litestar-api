from datetime import datetime

from litestar import Controller, delete, get, post, put
from litestar.exceptions import NotFoundException
from sqlalchemy import delete as sql_delete
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from todos.adapters import orm
from todos.adapters.repositories import TodoRepository
from todos.domain.schemas import CreateTodo, Todo, UpdateTodo
from todos.service_layer.services import TodoService


class TodoController(Controller):
    @get()
    async def list_todos(self, transaction: AsyncSession) -> list[Todo]:
        todo_service = TodoService(TodoRepository(transaction))
        todo_list = []
        print(1)
        for todo in await todo_service.get_list():
            todo_list.append(Todo.model_validate(todo))
        print(2)
        return todo_list

    @get("/{todo_id: int}")
    async def retrieve_todo(self, transaction: AsyncSession, todo_id: int) -> Todo:
        query = select(orm.Todo).where(orm.Todo.id == todo_id)
        result = await transaction.execute(query)
        todo = result.scalars().first()
        if not todo:
            raise NotFoundException
        return Todo.model_validate(todo)

    @post("")
    async def create_todo(self, transaction: AsyncSession, data: CreateTodo) -> Todo:
        query = orm.Todo(
            content=data.content,
            is_completed=False,
            order=data.order,
            created_at=datetime.now(),
            updated_at=datetime.now(),
        )
        transaction.add(query)
        await transaction.commit()
        return Todo.model_validate(query)

    @put("/{todo_id: int}")
    async def update_todo(
        self, transaction: AsyncSession, todo_id: int, data: UpdateTodo
    ) -> Todo:
        query = select(orm.Todo).where(orm.Todo.id == todo_id)
        result = await transaction.execute(query)
        todo = result.scalars().first()
        todo.content = data.content
        todo.is_completed = data.is_completed
        todo.order = data.order
        todo.updated_at = datetime.now()
        await transaction.commit()
        return Todo.model_validate(todo)

    @delete("/{todo_id: int}")
    async def delete_todo(self, transaction: AsyncSession, todo_id: int) -> None:
        query = select(orm.Todo).where(orm.Todo.id == todo_id)
        result = await transaction.execute(query)
        todo = result.scalars().first()
        if not todo:
            raise NotFoundException
        await transaction.execute(sql_delete(orm.Todo).where(orm.Todo.id == todo_id))
        await transaction.commit()
        return None
