import logging

from telegram.ext import ContextTypes

from handlers.bot_handlers import t
from services.users import get_user_language

logger = logging.getLogger(__name__)

async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE):
    logger.error("Exception while handling update:", exc_info=context.error)

    if update and hasattr(update, "effective_user"):
        user_id = update.effective_user.id

        try:
            lang = await get_user_language(user_id)
        except Exception:
            logger.exception("Failed to get user language")
            lang = "ru"

        try:
            await update.effective_message.reply_text(t(lang, "error"))
        except Exception:
                logger.exception("Failed to send error message to user")
