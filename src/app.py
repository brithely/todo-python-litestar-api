from litestar import Litestar, Router

from databases import db_connection, provide_transaction
from todos.endpoints.routes import TodoController

todo_route = Router(path="/todo", route_handlers=[TodoController])


app = Litestar(
    route_handlers=[todo_route],
    dependencies={"transaction": provide_transaction},
    lifespan=[db_connection],
)
