from datetime import datetime

from todos.adapters.repositories import TodoRepository
from todos.domain.schemas import CreateTodo, Todo, UpdateTodo


class TodoService:
    def __init__(self, repo: TodoRepository):
        self.repo = repo

    async def get(self, todo_id: int) -> Todo:
        return Todo.model_validate(await self.repo.get(todo_id))

    async def get_list(self) -> list[Todo]:
        todo_list = [Todo.model_validate(todo) for todo in await self.repo.get_list()]
        return todo_list

    async def create(self, data: CreateTodo) -> Todo:
        create_data = {
            "content": data.content,
            "is_completed": False,
            "order": data.order,
            "created_at": datetime.now(),
            "updated_at": datetime.now(),
        }
        return Todo.model_validate(await self.repo.create(data=create_data))

    async def update(self, todo_id: int, data: UpdateTodo) -> Todo:
        update_data = {
            "content": data.content,
            "is_completed": data.is_completed,
            "order": data.order,
            "updated_at": datetime.now(),
        }
        return Todo.model_validate(
            await self.repo.update(todo_id=todo_id, data=update_data)
        )

    async def delete(self, todo_id: int) -> bool:
        return await self.repo.delete(todo_id)
