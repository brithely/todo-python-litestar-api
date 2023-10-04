from os import environ
from typing import Any
from uuid import UUID

from litestar import Litestar, Request, Response, get, post
from litestar.connection import ASGIConnection
from litestar.contrib.jwt import JWTCookieAuth, Token
from litestar.openapi.config import OpenAPIConfig
from pydantic import BaseModel, EmailStr


# Let's assume we have a User model that is a pydantic model.
# This though is not required - we need some sort of user class -
# but it can be any arbitrary value, e.g. an SQLAlchemy model, a representation of a MongoDB  etc.
class User(BaseModel):
    id: UUID
    name: str
    email: EmailStr


MOCK_DB: dict[str, User] = {
    "29fa0c27-8b6b-4bcc-9525-4a090ccef861": User(
        id="29fa0c27-8b6b-4bcc-9525-4a090ccef861",
        name="John Doe",
        email="test@test.com",
    ),
}


# JWTCookieAuth requires a retrieve handler callable that receives the JWT token model and the ASGI connection
# and returns the 'User' instance correlating to it.
#
# Notes:
# - 'User' can be any arbitrary value you decide upon.
# - The callable can be either sync or async - both will work.
async def retrieve_user_handler(
    token: "Token", connection: "ASGIConnection[Any, Any, Any, Any]"
) -> User | None:
    # logic here to retrieve the user instance
    return MOCK_DB.get(token.sub)


jwt_cookie_auth = JWTCookieAuth[User](
    retrieve_user_handler=retrieve_user_handler,
    token_secret=environ.get("JWT_SECRET", "abcd123"),
    # we are specifying which endpoints should be excluded from authentication. In this case the login endpoint
    # and our openAPI docs.
    exclude=["/login", "/schema"],
    # Tip: We can optionally supply cookie options to the configuration.  Here is an example of enabling the secure cookie option
    # auth_cookie_options=CookieOptions(secure=True),
)


# Given an instance of 'JWTCookieAuth' we can create a login handler function:
@post("/login")
async def login_handler(data: "User") -> "Response[User]":
    MOCK_DB[str(data.id)] = data
    return jwt_cookie_auth.login(identifier=str(data.id), response_body=data)


@get("/test")
async def test_handler() -> str:
    return "test"
