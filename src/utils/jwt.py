from os import environ
from typing import Any

from litestar.connection import ASGIConnection
from litestar.contrib.jwt import JWTAuth, Token

from users.domain.schemas import User


async def retrieve_user_handler(
    token: "Token", connection: "ASGIConnection[Any, Any, Any, Any]"
) -> User | None:
    # logic here to retrieve the user instance
    return


jwt_auth = JWTAuth[User](
    retrieve_user_handler=retrieve_user_handler,
    token_secret=environ.get("JWT_SECRET", "abcd123"),
    # we are specifying which endpoints should be excluded from authentication. In this case the login endpoint
    # and our openAPI docs.
    exclude=["/login", "/schema"],
)
