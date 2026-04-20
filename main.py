import logging
import random
import os
from collections import defaultdict

from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ConversationHandler, 
    ContextTypes,
    filters
)


TEXTS = {
    "ru": {
        "start": "Привет! Я бот-рандомайзер 🎲\n\n"
                 "Я помогу тебе случайно выбрать что-нибудь из вариантов.\n\n"
                 "Команды:\n"
                 "/add – добавить варианты\n"
                 "/list – показать текущие варианты\n"
                 "/random – случайно выбрать\n"
                 "/clear – очистить список\n"
                 "/language – сменить язык",

        "choose_lang": "Выбери язык:",
        "add_prompt": "Ок! Отправляй варианты по одному. Когда закончишь – /done.",
        "added": "Добавил вариант: «{option}»",
        "done": "Готово! Теперь используй /random.",
        "empty": "Список пуст. Напиши /add.",
        "list": "Твои варианты:\n\n{options}",
        "random": "🎲 Случайный выбор: «{choice}»",
        "cleared": "Я очистил список.",
        "cancel": "Отменил.",
    },

    "en": {
        "start": "Hi! I am a randomizer bot 🎲\n\n"
                 "I can help you randomly choose.\n\n"
                 "Commands:\n"
                 "/add – add options\n"
                 "/list – show options\n"
                 "/random – choose randomly\n"
                 "/clear – clear list\n"
                 "/language – change language",

        "choose_lang": "Choose a language:",
        "add_prompt": "Send options one by one. When done – /done.",
        "added": "Added option: \"{option}\"",
        "done": "Done! Use /random.",
        "empty": "List is empty. Use /add.",
        "list": "Your options:\n\n{options}",
        "random": "🎲 Random choice: \"{choice}\"",
        "cleared": "List cleared.",
        "cancel": "Cancelled.",
    }
}


CHOOSING_LANGUAGE = 0
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

def t(lang: str, key: str, **kwargs) -> str:
    text = TEXTS.get(lang, TEXTS["ru"]).get(key, key)
    return text.format(**kwargs)


async def language(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [["Русский🇷🇺", "English🇬🇧"]]
    await update.message.reply_text(
        "Выбери язык / Choose a language:",
        reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=True)
    )
    return CHOOSING_LANGUAGE


async def set_language(update: Update, context: ContextTypes.DEFAULT_TYPE):
    choice = update.message.text.strip()

    if choice == "Русский🇷🇺":
        context.user_data["lang"] = "ru"
        lang = context.user_data["lang"]
        await update.message.reply_text(t(lang, "start"))

    elif choice == "English🇬🇧":
        context.user_data["lang"] = "en"
        lang = context.user_data["lang"]
        await update.message.reply_text(t(lang, "start"))
    else:
        await update.message.reply_text("Пожалуйста, выбери язык кнопкой / Please use the buttons.")
        return CHOOSING_LANGUAGE

    return ConversationHandler.END


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lang = context.user_data.get("lang")

    if not lang:
        keyboard = [["Русский🇷🇺", "English🇬🇧"]]
        await update.message.reply_text(
            "Выбери язык / Choose a language:",
            reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
        )
        return CHOOSING_LANGUAGE

    await update.message.reply_text(t(lang, "start"))

async def add(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Включаем режим добавления вариантов.
    """
    lang = context.user_data.get("lang", "ru")
    await update.message.reply_text(t(lang, "add_prompt"))
    return ADDING_OPTIONS


async def add_option(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    lang = context.user_data.get("lang", "ru")

    option = update.message.text.strip()

    if option.startswith("/"):
        return ADDING_OPTIONS

    user_options[user_id].append(option)

    await update.message.reply_text(t(lang, "added", option=option))
    return ADDING_OPTIONS


async def done(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    lang = context.user_data.get("lang", "ru")

    if not user_options[user_id]:
        await update.message.reply_text(t(lang, "empty"))
    else:
        await update.message.reply_text(t(lang, "done"))

    return ConversationHandler.END


async def list_options(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    lang = context.user_data.get("lang", "ru")

    opts = user_options[user_id]

    if not opts:
        await update.message.reply_text(t(lang, "empty"))
        return

    text = "\n".join(f"{i+1}. {opt}" for i, opt in enumerate(opts))
    await update.message.reply_text(t(lang, "list", options=text))


async def random_choice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    lang = context.user_data.get("lang", "ru")

    opts = user_options[user_id]

    if not opts:
        await update.message.reply_text(t(lang, "empty"))
        return

    choice = random.choice(opts)
    await update.message.reply_text(t(lang, "random", choice=choice))


async def clear(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    lang = context.user_data.get("lang", "ru")

    user_options[user_id].clear()
    await update.message.reply_text(t(lang, "cleared"))


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lang = context.user_data.get("lang", "ru")
    await update.message.reply_text(t(lang, "cancel"))
    return ConversationHandler.END

def main():
    application = ApplicationBuilder().token(BOT_TOKEN).build()

    lang_handler = ConversationHandler(
        entry_points=[CommandHandler("language", language)],
        states={
            CHOOSING_LANGUAGE: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, set_language),
            ],
        },
        fallbacks=[],
    )
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
    application.add_handler(lang_handler)
    application.add_handler(CommandHandler("list", list_options))
    application.add_handler(CommandHandler("random", random_choice))
    application.add_handler(CommandHandler("clear", clear))

    application.run_polling()

if __name__ == "__main__":
    main()
