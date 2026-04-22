from sqlalchemy import select
from database import AsyncSessionLocal
from models import User


async def get_or_create_user(telegram_user_id: int) -> User:
    async with AsyncSessionLocal() as session:
        result = await session.execute(
            select(User).where(User.telegram_user_id == telegram_user_id)
        )
        user = result.scalar_one_or_none()

        if user is None:
            user = User(telegram_user_id=telegram_user_id)
            session.add(user)
            await session.commit()
            await session.refresh(user)

        return user


async def set_user_language(telegram_user_id: int, language: str) -> None:
    async with AsyncSessionLocal() as session:
        result = await session.execute(
            select(User).where(User.telegram_user_id == telegram_user_id)
        )
        user = result.scalar_one_or_none()

        if user is None:
            user = User(telegram_user_id=telegram_user_id, language=language)
            session.add(user)
        else:
            user.language = language

        await session.commit()


async def get_user_language(telegram_user_id: int) -> str:
    async with AsyncSessionLocal() as session:
        result = await session.execute(
            select(User.language).where(User.telegram_user_id == telegram_user_id)
        )
        language = result.scalar_one_or_none()
        return language or "ru"