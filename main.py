import logging
import random
import os
from collections import defaultdict
from dotenv import load_dotenv

from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ConversationHandler, 
    ContextTypes,
    filters
)

load_dotenv()

ADDING_OPTIONS = 1

BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    raise ValueError('Bot is not founded')

user_options = defaultdict(list)

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
# set higher logging level for httpx to avoid all GET and POST requests being logged
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "Привет! Я бот-рандомайзер 🎲\n\n"
        "Я помогу тебе случайно выбрать что-нибудь из вариантов.\n\n"
        "Команды:\n"
        "/add – добавить варианты\n"
        "/list – показать текущие варианты\n"
        "/random – случайно выбрать один из вариантов\n"
        "/clear – удалить все варианты\n"
    )
    await update.message.reply_text(text)

async def add(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Включаем режим добавления вариантов.
    """
    await update.message.reply_text(
        "Ок! Отправляй мне варианты по одному в каждом сообщении.\n"
        "Когда закончишь – напиши /done."
    )
    return ADDING_OPTIONS


async def add_option(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Обрабатываем каждое текстовое сообщение как новый вариант.
    """
    user_id = update.effective_user.id
    option = update.message.text.strip()

    # Игнорируем команды, если вдруг кто-то напишет
    if option.startswith("/"):
        await update.message.reply_text(
            "Если ты закончил добавлять варианты – напиши /done."
        )
        return ADDING_OPTIONS

    user_options[user_id].append(option)
    await update.message.reply_text(f"Добавил вариант: «{option}»")
    return ADDING_OPTIONS


async def done(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Выход из режима добавления.
    """
    user_id = update.effective_user.id
    opts = user_options[user_id]

    if not opts:
        await update.message.reply_text(
            "Ты не добавил ни одного варианта. Можешь снова написать /add."
        )
    else:
        await update.message.reply_text(
            "Готово! Варианты сохранены.\n"
            "Теперь можешь использовать /random, чтобы случайно выбрать."
        )

    return ConversationHandler.END


async def list_options(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    opts = user_options[user_id]

    if not opts:
        await update.message.reply_text("Список вариантов пуст. Напиши /add, чтобы добавить.")
        return

    text = "Твои текущие варианты:\n\n"
    text += "\n".join(f"{i+1}. {opt}" for i, opt in enumerate(opts))
    await update.message.reply_text(text)


async def random_choice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    opts = user_options[user_id]

    if not opts:
        await update.message.reply_text(
            "Список вариантов пуст. Сначала добавь варианты командой /add."
        )
        return

    choice = random.choice(opts)
    await update.message.reply_text(f"🎲 Случайный выбор: «{choice}»")


async def clear(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user_options[user_id].clear()
    await update.message.reply_text("Я очистил твой список вариантов.")


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Ок, отменил добавление вариантов.")
    return ConversationHandler.END

def main():
    application = ApplicationBuilder().token(BOT_TOKEN).build()
# Обработчик диалога для добавления вариантов
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("add", add)],
        states={
            ADDING_OPTIONS: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, add_option),
                CommandHandler("done", done),
            ],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )

    application.add_handler(CommandHandler("start", start))
    application.add_handler(conv_handler)
    application.add_handler(CommandHandler("list", list_options))
    application.add_handler(CommandHandler("random", random_choice))
    application.add_handler(CommandHandler("clear", clear))

    application.run_polling()

if __name__ == "__main__":
    main()
