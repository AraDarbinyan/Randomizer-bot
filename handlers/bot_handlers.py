import random

from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes, ConversationHandler

from config import TEXTS, MAX_OPTION_LENGTH, MAX_OPTIONS_PER_USER
from services.users import get_user_language, set_user_language
from services.options import *


CHOOSING_LANGUAGE = 0
ADDING_OPTIONS = 1

def t(lang: str, key: str, **kwargs) -> str:
    text = TEXTS.get(lang, TEXTS["ru"]).get(key, key)
    return text.format(**kwargs)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    lang = await get_user_language(user_id)

    if not lang:
        keyboard = [["Русский🇷🇺", "English🇬🇧"],
                    ["🇩🇪 Deutsch", "🇪🇸 Español"]]
        await update.message.reply_text(
            "Выбери язык / Choose a language:",
            reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
        )
        return CHOOSING_LANGUAGE

    await update.message.reply_text(t(lang, "start"))

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    lang = await get_user_language(user_id)

    await update.message.reply_text(t(lang, "help"))


async def language(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [["🇷🇺 Русский", "🇬🇧 English"],
                ["🇩🇪 Deutsch", "🇪🇸 Español"]]
    await update.message.reply_text(
        "Выбери язык / Choose a language:",
        reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    )
    return CHOOSING_LANGUAGE


async def set_language(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    choice = update.message.text.strip()

    if "Русский" in choice:
        lang = "ru"
    elif "English" in choice:
        lang = "en"
    elif "Deutsch" in choice:
        lang = "de"
    elif "Español" in choice:
        lang = "es"
    else:
        await update.message.reply_text(
            "Пожалуйста, выбери язык кнопкой / Please choose a language using the buttons."
        )
        return CHOOSING_LANGUAGE

    await set_user_language(user_id, lang)

    await update.message.reply_text(
        t(lang, "start"),
        reply_markup=ReplyKeyboardRemove()
    )

    return ConversationHandler.END


async def add(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    lang = await get_user_language(user_id)

    await update.message.reply_text(t(lang, "add_prompt"))
    return ADDING_OPTIONS



async def add_option(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    lang = await get_user_language(user_id)

    option = update.message.text.strip()

    if option.startswith("/"):
        return ADDING_OPTIONS

    if len(option) > MAX_OPTION_LENGTH:
        await update.message.reply_text(
            t(lang, "option_too_long", max=MAX_OPTION_LENGTH)
        )
        return ADDING_OPTIONS

    count = await count_user_options(user_id)

    if count >= MAX_OPTIONS_PER_USER:
        await update.message.reply_text(
            t(lang, "options_limit", max=MAX_OPTIONS_PER_USER)
        )
        return ADDING_OPTIONS

    await add_option_for_user(user_id, option)

    await update.message.reply_text(
        t(lang, "added", option=option)
    )

    return ADDING_OPTIONS


async def done(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    lang = await get_user_language(user_id)

    await update.message.reply_text(t(lang, "done"))
    return ConversationHandler.END


async def list_options(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    lang = await get_user_language(user_id)

    opts = await get_user_options(user_id)

    if not opts:
        await update.message.reply_text(t(lang, "empty"))
        return

    text = "\n".join(f"{i+1}. {opt}" for i, opt in enumerate(opts))
    await update.message.reply_text(t(lang, "list", options=text))


async def random_choice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    lang = await get_user_language(user_id)

    opts = await get_user_options(user_id)

    if not opts:
        await update.message.reply_text(t(lang, "empty"))
        return

    choice = random.choice(opts)
    await update.message.reply_text(t(lang, "random", choice=choice))


async def clear(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    lang = await get_user_language(user_id)

    await clear_user_options(user_id)

    await update.message.reply_text(t(lang, "cleared"))

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    lang = await get_user_language(user_id)

    await update.message.reply_text(t(lang, "cancel"))
    return ConversationHandler.END

async def remove_option(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    lang = await get_user_language(user_id)

    options = await get_user_options_with_ids(user_id)

    if not options:
        await update.message.reply_text(t(lang, "remove_empty"))
        return

    keyboard = []

    row = []

    for option_id, option_text in options:
        row.append(
            InlineKeyboardButton(
                text=option_text,
                callback_data=f"remove:{option_id}"
            )
        )

        if len(row) == 2:
            keyboard.append(row)
            row = []


    if row:
        keyboard.append(row)

    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        t(lang, "remove_choose"),
        reply_markup=reply_markup
    )

async def remove_option_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    user_id = query.from_user.id
    lang = await get_user_language(user_id)

    data = query.data

    if not data.startswith("remove:"):
        return

    option_id = int(data.split(":")[1])

    removed_option = await remove_option_by_id(user_id, option_id)

    if removed_option is None:
        await query.edit_message_text(t(lang, "remove_not_found"))
        return

    await query.edit_message_text(
        t(lang, "remove_success", option=removed_option)
    )