from litestar.testing import TestClient

from src.todos.domain.schemas import Todo
from src.todos.service_layer.services import TodoService


def test_todo_get_api_would_return_todo(
    client: TestClient, todo_service: TodoService, todo: Todo
) -> None:
    todo_id = 1
    todo_service().create(todo=todo)
    response = client.get(f"/todo/{todo_id}")
    assert response.status_code == 200
    assert response.json() == dict(todo)
