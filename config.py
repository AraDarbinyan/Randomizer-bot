import os 

BOT_TOKEN = os.getenv("BOT_TOKEN")

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "sqlite+aiosqlite:///./bot.db"
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
