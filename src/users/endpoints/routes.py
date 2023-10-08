from litestar import Controller, Response, post
from sqlalchemy.ext.asyncio import AsyncSession

from users.adapters.repository import UserRepo
from users.domain.schemas import User, UserLogin, UserSignup
from users.service_layer.services import UserService


class UserController(Controller):
    @post("/login")
    async def login(
        self, transaction: AsyncSession, data: "UserLogin"
    ) -> "Response[User]":
        return await UserService(UserRepo(transaction)).login(data.email, data.password)

    @post("signup")
    async def signup(self, transaction: AsyncSession, data: UserSignup) -> User:
        return await UserService(UserRepo(transaction)).signup(data)
