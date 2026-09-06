from unittest.mock import AsyncMock

import pytest
from telegram import BotCommandScopeChat

from bot_commands import COMMANDS, set_user_commands

EXPECTED_COMMANDS = {
    "start",
    "add",
    "list",
    "random",
    "remove",
    "clear",
    "language",
    "help",
}


def test_all_supported_languages_exist():
    assert set(COMMANDS) == {"ru", "en", "de", "es"}


@pytest.mark.parametrize("lang", ["ru", "en", "de", "es"])
def test_all_languages_have_expected_commands(lang):
    commands = {command.command for command in COMMANDS[lang]}

    assert commands == EXPECTED_COMMANDS


@pytest.mark.parametrize("lang", ["ru", "en", "de", "es"])
def test_all_commands_have_descriptions(lang):
    for command in COMMANDS[lang]:
        assert command.description.strip()


@pytest.mark.asyncio
async def test_set_user_commands_uses_selected_language():
    bot = AsyncMock()
    chat_id = 123456

    await set_user_commands(bot, chat_id, "ru")

    bot.set_my_commands.assert_awaited_once()

    args = bot.set_my_commands.await_args

    assert args.args[0] == COMMANDS["ru"]

    scope = args.kwargs["scope"]

    assert isinstance(scope, BotCommandScopeChat)
    assert scope.chat_id == chat_id


@pytest.mark.asyncio
async def test_set_user_commands_falls_back_to_english():
    bot = AsyncMock()

    await set_user_commands(bot, 123456, "unknown")

    commands = bot.set_my_commands.await_args.args[0]

    assert commands == COMMANDS["en"]
