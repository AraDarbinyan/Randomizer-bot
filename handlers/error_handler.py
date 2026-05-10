from telegram.ext import ContextTypes
from services.users import get_user_language
from handlers.bot_handlers import t
import logging

logger = logging.getLogger(__name__)

async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE):
    logger.error("Exception while handling update:", exc_info=context.error)

    if update and hasattr(update, "effective_user"):
        user_id = update.effective_user.id

        try:
            lang = await get_user_language(user_id)
        except:
            lang = "ru"

        try:
            await update.effective_message.reply_text(t(lang, "error"))
        except:
            pass