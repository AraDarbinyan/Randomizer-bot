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
                 "/help – помощь\n"
                 "/list – показать текущие варианты\n"
                 "/random – случайно выбрать\n"
                 "/clear – очистить список\n"
                 "/language – сменить язык",

        "help": 
                "Команды:\n"
                        "/start – главное меню\n"
                        "/help – помощь\n"
                        "/language – сменить язык\n"
                        "/add – добавить варианты\n"
                        "/done – завершить добавление\n"
                        "/list – показать варианты\n"
                        "/random – случайный выбор\n"
                        "/remove <номер> – удалить вариант\n"
                        "/clear – очистить список\n"
                        "/cancel – отменить действие"
                ,

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
                 "/help – help\n"
                 "/add – add options\n"
                 "/list – show options\n"
                 "/random – choose randomly\n"
                 "/clear – clear list\n"
                 "/language – change language",

        "help": 
                    "Commands:\n"
                    "/start – main menu\n"
                    "/help – help\n"
                    "/language – change language\n"
                    "/add – add options\n"
                    "/done – finish adding\n"
                    "/list – show options\n"
                    "/random – random choice\n"
                    "/remove <number> – remove option\n"
                    "/clear – clear list\n"
                    "/cancel – cancel action"
                ,

        "choose_lang": "Choose a language:",
        "add_prompt": "Send options one by one. When done – /done.",
        "added": "Added option: \"{option}\"",
        "done": "Done! Use /random.",
        "empty": "List is empty. Use /add.",
        "list": "Your options:\n\n{options}",
        "random": "🎲 Random choice: \"{choice}\"",
        "cleared": "List cleared.",
        "cancel": "Cancelled.",
    },

    "de": {
        "start": "Hallo! Ich bin ein Zufallsbot 🎲\n\n"
                 "Ich helfe dir, zufällig etwas auszuwählen.\n\n"
                 "Befehle:\n"
                 "/help – Hilfe\n"
                 "/add – Optionen hinzufügen\n"
                 "/list – Liste anzeigen\n"
                 "/random – zufällig wählen\n"
                 "/clear – Liste löschen\n"
                 "/language – Sprache ändern",
        "help": 
                "Befehle:\n"
                "/start – Hauptmenü\n"
                "/help – Hilfe\n"
                "/language – Sprache ändern\n"
                "/add – Optionen hinzufügen\n"
                "/done – Hinzufügen beenden\n"
                "/list – Optionen anzeigen\n"
                "/random – zufällig auswählen\n"
                "/remove <Nummer> – Option entfernen\n"
                "/clear – Liste löschen\n"
                "/cancel – Aktion abbrechen"
            ,

        "add_prompt": "Sende Optionen einzeln. Wenn fertig – /done.",
        "added": "Option hinzugefügt: \"{option}\"",
        "done": "Fertig!",
        "empty": "Liste ist leer.",
        "list": "Deine Optionen:\n\n{options}",
        "random": "🎲 Zufällige Auswahl: \"{choice}\"",
        "cleared": "Liste gelöscht.",
        "cancel": "Abgebrochen.",
    },

    "es": {
        "start": "¡Hola! Soy un bot aleatorio 🎲\n\n"
                 "Puedo ayudarte a elegir algo al azar.\n\n"
                 "Comandos:\n"
                 "/help – ayuda\n"
                 "/add – añadir opciones\n"
                 "/list – mostrar lista\n"
                 "/random – elegir al azar\n"
                 "/clear – limpiar lista\n"
                 "/language – cambiar idioma",
        "help": 
                "Comandos:\n"
                "/start – menú principal\n"
                "/help – ayuda\n"
                "/language – cambiar idioma\n"
                "/add – añadir opciones\n"
                "/done – terminar de añadir\n"
                "/list – mostrar opciones\n"
                "/random – elegir al azar\n"
                "/remove <número> – eliminar opción\n"
                "/clear – limpiar lista\n"
                "/cancel – cancelar acción"
            ,

        "add_prompt": "Envía opciones una por una. Cuando termines – /done.",
        "added": "Opción añadida: \"{option}\"",
        "done": "¡Listo!",
        "empty": "La lista está vacía.",
        "list": "Tus opciones:\n\n{options}",
        "random": "🎲 Elección aleatoria: \"{choice}\"",
        "cleared": "Lista limpiada.",
        "cancel": "Cancelado.",
    }
}
