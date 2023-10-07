from sqlalchemy import insert, select

from users.adapters.orm import User


class UserRepo:
    def __init__(self, session):
        self.session = session

    async def get_by_email(self, email: str) -> User:
        query = select(User).where(User.email == email).limit(1)
        result = await self.session.execute(query)
        return result.scalars().first()

    async def create(self, data: dict) -> User:
        query = insert(User).values(**data).returning(User)
        result = await self.session.execute(query)
        return result.scalars().first()
