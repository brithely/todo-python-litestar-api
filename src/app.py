from litestar import Litestar, Router

from databases import db_connection, provide_transaction
from todos.endpoints.routes import TodoController
from users.endpoints.routes import UserController

todo_route = Router(path="/todos", route_handlers=[TodoController])
user_route = Router(path="/users", route_handlers=[UserController])


app = Litestar(
    debug=True,
    route_handlers=[
        todo_route,
        user_route,
    ],
    dependencies={"transaction": provide_transaction},
    lifespan=[db_connection],
)
