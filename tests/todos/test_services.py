# from datetime import datetime

# from src.todos.domain.schemas import Todo
# from src.todos.service_layer.services import TodoService


# def test_todo_service_get(todo_service: TodoService) -> None:
#     todo_id = 1
#     todo = Todo(
#         id=1,
#         content="test",
#         is_completed=False,
#         order=1,
#         created_at=datetime.now(),
#         updated_at=datetime.now(),
#     )
#     assert todo_service.get(todo_id=todo_id) == todo
