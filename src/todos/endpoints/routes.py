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
        return await todo_service.get_list()

    @get("/{todo_id: int}")
    async def retrieve_todo(self, transaction: AsyncSession, todo_id: int) -> Todo:
        todo_service = TodoService(TodoRepository(transaction))
        return await todo_service.get(todo_id)

    @post("")
    async def create_todo(self, transaction: AsyncSession, data: CreateTodo) -> Todo:
        todo_service = TodoService(TodoRepository(transaction))
        return await todo_service.create(data)

    @put("/{todo_id: int}")
    async def update_todo(
        self, transaction: AsyncSession, todo_id: int, data: UpdateTodo
    ) -> Todo:
        todo_service = TodoService(TodoRepository(transaction))
        return await todo_service.update(todo_id, data)

    @delete("/{todo_id: int}")
    async def delete_todo(self, transaction: AsyncSession, todo_id: int) -> None:
        todo_service = TodoService(TodoRepository(transaction))
        if not await todo_service.delete(todo_id):
            raise NotFoundException()
        return None
