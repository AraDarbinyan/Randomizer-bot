# Randomizer Telegram Bot

A multilingual Telegram bot for creating, managing, and randomly selecting options from custom user lists.

Built with:
- Python
- python-telegram-bot
- SQLAlchemy Async ORM
- SQLite (development)
- PostgreSQL-ready architecture

---

# Features

- Multilingual support:
  - English
  - Russian
  - German
  - Spanish

- Add custom options
- View saved options
- Random choice selection
- Remove options with inline buttons
- Clear all options
- Input validation
- Async architecture
- Database persistence
- Error handling and logging

---

# Commands

| Command | Description |
|---|---|
| /start | Start the bot |
| /help | Show help message |
| /language | Change language |
| /add | Add options |
| /done | Finish adding options |
| /list | Show all options |
| /random | Pick a random option |
| /remove | Remove an option using inline buttons |
| /clear | Clear all options |
| /cancel | Cancel current action |

---

# Tech Stack

- Python 3.12+
- python-telegram-bot v20+
- SQLAlchemy Async
- SQLite + aiosqlite
- PostgreSQL-ready architecture

---

# Project Structure

telegram-randomizer-bot/
├── handlers/
│   |── bot_handlers.py
|   └── error_handlers.py
├── services/
│   ├── options.py
│   └── users.py
├── database.py
├── models.py
├── config.py
├── main.py
├── requirements.txt
└── README.md

---

# Installation

## 1. Clone repository

git clone https://github.com/YOUR_USERNAME/YOUR_REPOSITORY.git
cd YOUR_REPOSITORY

---

## 2. Create virtual environment

### Linux / macOS

python3 -m venv venv
source venv/bin/activate

### Windows

python -m venv venv
venv\Scripts\activate

---

## 3. Install dependencies

pip install -r requirements.txt

---

# Environment Variables

Create a .env file or configure environment variables.

Example:

BOT_TOKEN=your_telegram_bot_token
DATABASE_URL=sqlite+aiosqlite:///./bot.db

---

# Run the Bot

python3 main.py

---

# Database

Current development database:
- SQLite (aiosqlite)

Production-ready:
- PostgreSQL (asyncpg)

To switch to PostgreSQL, simply change:

DATABASE_URL

Example:

DATABASE_URL=postgresql+asyncpg://user:password@host:port/dbname

---

# Validation

The bot includes:
- maximum option length validation
- maximum options per user validation
- command validation
- error handling and logging

---

# Future Improvements

- PostgreSQL deployment
- Docker support
- Pagination for large option lists
- Inline menus for all actions
- Statistics system
- User profiles
- Admin panel

---

# License

This project is open-source and available under the MIT License.