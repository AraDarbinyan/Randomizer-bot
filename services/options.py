from sqlalchemy import select, delete
from db.database import AsyncSessionLocal
from db.models import User, Option
from sqlalchemy import select, func

async def count_user_options(telegram_user_id: int) -> int:
    async with AsyncSessionLocal() as session:
        result = await session.execute(
            select(func.count(Option.id))
            .join(User, Option.user_id == User.id)
            .where(User.telegram_user_id == telegram_user_id)
        )
        return result.scalar_one()


async def add_option_for_user(telegram_user_id: int, text: str) -> None:
    async with AsyncSessionLocal() as session:
        result = await session.execute(
            select(User).where(User.telegram_user_id == telegram_user_id)
        )
        user = result.scalar_one_or_none()

        if user is None:
            user = User(telegram_user_id=telegram_user_id)
            session.add(user)
            await session.flush()

        option = Option(user_id=user.id, text=text)
        session.add(option)
        await session.commit()


async def get_user_options(telegram_user_id: int) -> list[str]:
    async with AsyncSessionLocal() as session:
        result = await session.execute(
            select(Option.text)
            .join(User, Option.user_id == User.id)
            .where(User.telegram_user_id == telegram_user_id)
            .order_by(Option.id)
        )
        return list(result.scalars().all())


async def clear_user_options(telegram_user_id: int) -> None:
    async with AsyncSessionLocal() as session:
        result = await session.execute(
            select(User).where(User.telegram_user_id == telegram_user_id)
        )
        user = result.scalar_one_or_none()

        if user is None:
            return

        await session.execute(delete(Option).where(Option.user_id == user.id))
        await session.commit()



async def get_user_options_with_ids(telegram_user_id: int) -> list[tuple[int, str]]:
    async with AsyncSessionLocal() as session:
        result = await session.execute(
            select(Option.id, Option.text)
            .join(User, Option.user_id == User.id)
            .where(User.telegram_user_id == telegram_user_id)
            .order_by(Option.id)
        )

        return list(result.all())
    
async def remove_option_by_id(telegram_user_id: int, option_id: int) -> str | None:
    async with AsyncSessionLocal() as session:
        result = await session.execute(
            select(Option)
            .join(User, Option.user_id == User.id)
            .where(
                User.telegram_user_id == telegram_user_id,
                Option.id == option_id
            )
        )

        option = result.scalar_one_or_none()

        if option is None:
            return None

        option_text = option.text

        await session.delete(option)
        await session.commit()

        return option_text