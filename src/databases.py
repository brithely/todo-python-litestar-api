import os
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from litestar import Litestar, status_codes
from litestar.datastructures import State
from litestar.exceptions import ClientException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import declarative_base, sessionmaker


def get_postgres_uri():
    host = os.environ.get("DB_HOST")
    port = os.environ.get("DB_PORT")
    password = os.environ.get("DB_PASSWORD")
    user = os.environ.get("DB_USER")
    db_name = os.environ.get("DB_DATABASE")
    return f"postgresql+psycopg://{user}:{password}@{host}:{port}/{db_name}"


@asynccontextmanager
async def db_connection(app: Litestar) -> AsyncGenerator[None, None]:
    engine = getattr(app.state, "engine", None)
    if engine is None:
        engine = create_async_engine(get_postgres_uri(), echo=True)
        app.state.engine = engine

    try:
        yield
    finally:
        await engine.dispose()



ModelBase = declarative_base()


sessionmaker = async_sessionmaker(expire_on_commit=False)


async def provide_transaction(state: State) -> AsyncGenerator[AsyncSession, None]:
    async with sessionmaker(bind=state.engine) as session:
        try:
            async with session.begin():
                yield session
        except IntegrityError as exc:
            raise ClientException(
                status_code=status_codes.HTTP_409_CONFLICT,
                detail=str(exc),
            ) from exc
