from todos.adapters.repositories import TodoRepository


class TodoService:
    def __init__(self, repo=TodoRepository):
        self.repo = repo

    def get(self, todo_id):
        return self.repo.get(todo_id)

    def get_list(self):
        return self.repo.get_list()

    def create(self, data):
        return self.repo.create(data)

    def update(self, todo_id, data):
        return self.repo.update(todo_id, data)
