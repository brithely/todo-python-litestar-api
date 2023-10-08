from litestar.exceptions import ValidationException

from users.adapters.repository import UserRepo
from users.domain.schemas import User, UserSignup
from utils.jwt import jwt_auth
from utils.password import get_password_salf, hash_password


class UserService:
    def __init__(self, repo: UserRepo):
        self.repo = repo

    def _verify_password(self, password, user: User) -> bool:
        salt = get_password_salf(user.password)
        return user.password == hash_password(password, salt)

    async def login(self, email, password) -> User:
        user_model = await self.repo.get_by_email(email)
        if not user_model:
            raise ValidationException("Invalid email or password")
        user = User.model_validate(user_model)

        if self._verify_password(password, user):
            return jwt_auth.login(
                identifier=str(user.id),
                send_token_as_response_body=True,
                response_body=user,
            )
        else:
            raise ValidationException("Invalid email or password")

    async def signup(self, data: UserSignup) -> User:
        user_model = await self.repo.get_by_email(data.email)
        if user_model:
            raise ValidationException("User with this email already exists")
        user = User.model_validate(
            await self.repo.create(
                data={
                    "name": data.name,
                    "email": data.email,
                    "password": hash_password(data.password),
                }
            )
        )
        return await self.login(user.email, data.password)
