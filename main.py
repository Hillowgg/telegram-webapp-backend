import os
from aiogram import Bot, F, Router, Dispatcher
from aiogram.filters.command import Command
from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    MenuButtonWebApp,
    Message,
    WebAppInfo,
)
import dotenv

dotenv.load_dotenv()

TOKEN = os.getenv("TOKEN")
my_router = Router()


@my_router.message(Command("start"))
async def command_start(message: Message, bot: Bot, base_url: str):

    await message.answer("""Hi!\nSend me any type of message to start.\nOr just send /webview""")


def main() -> None:
    # Initialize Bot instance with an default parse mode which will be passed to all API calls
    bot = Bot(TOKEN, parse_mode="HTML")
    # And the run events dispatching
    dp = Dispatcher()
    dp.include_router(my_router)
    dp.run_polling(bot)


if __name__ == "__main__":
    main()
