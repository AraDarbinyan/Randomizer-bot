from telegram import BotCommand, BotCommandScopeChat

COMMANDS = {
    "ru": [
        BotCommand("start", "Запустить бота"),
        BotCommand("add", "Добавить варианты"),
        BotCommand("done", "Завершить добавление"),
        BotCommand("list", "Показать мои варианты"),
        BotCommand("random", "Выбрать случайный вариант"),
        BotCommand("remove", "Удалить вариант"),
        BotCommand("clear", "Удалить все варианты"),
        BotCommand("language", "Изменить язык"),
        BotCommand("help", "Помощь"),
    ],

    "en": [
        BotCommand("start", "Start the bot"),
        BotCommand("add", "Add options"),
        BotCommand("done", "Finish adding options"),
        BotCommand("list", "Show my options"),
        BotCommand("random", "Choose a random option"),
        BotCommand("remove", "Remove an option"),
        BotCommand("clear", "Remove all options"),
        BotCommand("language", "Change language"),
        BotCommand("help", "Help"),
    ],

    "de": [
        BotCommand("start", "Bot starten"),
        BotCommand("add", "Optionen hinzufügen"),
        BotCommand("done", "Hinzufügen beenden"),
        BotCommand("list", "Meine Optionen anzeigen"),
        BotCommand("random", "Zufällige Option auswählen"),
        BotCommand("remove", "Option entfernen"),
        BotCommand("clear", "Alle Optionen löschen"),
        BotCommand("language", "Sprache ändern"),
        BotCommand("help", "Hilfe"),
    ],

    "es": [
        BotCommand("start", "Iniciar el bot"),
        BotCommand("add", "Añadir opciones"),
        BotCommand("done", "Terminar de añadir"),
        BotCommand("list", "Mostrar mis opciones"),
        BotCommand("random", "Elegir una opción al azar"),
        BotCommand("remove", "Eliminar una opción"),
        BotCommand("clear", "Eliminar todas las opciones"),
        BotCommand("language", "Cambiar idioma"),
        BotCommand("help", "Ayuda"),
    ],
}


async def set_default_commands(application):
    """Set default commands for users before their language is known."""
    await application.bot.set_my_commands(COMMANDS["en"])


async def set_user_commands(bot, chat_id: int, lang: str):
    """Set command menu for a specific chat according to selected language."""

    commands = COMMANDS.get(lang, COMMANDS["en"])

    await bot.set_my_commands(
        commands,
        scope=BotCommandScopeChat(chat_id=chat_id),
    )
