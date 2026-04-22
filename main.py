import logging
import asyncio
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ConversationHandler,
    filters
)

from config import BOT_TOKEN
from handlers.bot_handlers import *
from db.database import engine
from db.models import Base


if not BOT_TOKEN:
    raise ValueError('Bot is not founded')


logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


def main():
    asyncio.run(init_db())

    app = ApplicationBuilder().token(BOT_TOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[
            CommandHandler("start", start),
            CommandHandler("language", language),
            CommandHandler("add", add),
        ],
        states={
            CHOOSING_LANGUAGE: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, set_language)
            ],
            ADDING_OPTIONS: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, add_option),
                CommandHandler("done", done),
            ],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )

    app.add_handler(conv_handler)
    app.add_handler(CommandHandler("list", list_options))
    app.add_handler(CommandHandler("random", random_choice))
    app.add_handler(CommandHandler("clear", clear))

    app.run_polling()


if __name__ == "__main__":
    main()
