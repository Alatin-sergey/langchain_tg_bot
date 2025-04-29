import asyncio
from aiogram.filters import CommandStart
from aiohttp import web, ClientSession
from aiogram.webhook.aiohttp_server import (
    SimpleRequestHandler, 
    setup_application,
)
from aiogram import Bot, Dispatcher, Router
from aiogram.types import Message
from dotenv import load_dotenv
import os

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
WEB_SERVER_HOST = os.getenv("WEB_SERVER_HOST")
WEB_SERVER_PORT = int(os.getenv("WEB_SERVER_PORT"))
WEBHOOK_PATH = os.getenv("WEBHOOK_PATH")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")
BACKEND_ENDPOINT = os.getenv("BACKEND_ENDPOINT")
CONNECTION_TYPE = os.getenv("CONNECTION_TYPE")

dp = Dispatcher()
bot = Bot(token=BOT_TOKEN)


async def on_startup(bot: Bot) -> None:
    await bot.set_webhook(
        url=f"{WEBHOOK_URL}{WEBHOOK_PATH}",
        allowed_updates=dp.resolve_used_update_types(),
        drop_pending_updates=True,
    )


@dp.message(CommandStart())
async def start_command_handler(message: Message) -> None:
    await message.answer(f"Привет, {message.from_user.first_name}! Я работаю на вебхуках.") # noqa: E501


@dp.message()
async def echo_answer(massege: Message) -> None:
    async with ClientSession() as session:
        response = await session.post(
            url=BACKEND_ENDPOINT, 
            json={"text": massege.text},
        )
        result = await response.json()
        response.close()
    await massege.answer(result["text"]) 


def main() -> None:
    dp.startup.register(on_startup)
    app = web.Application()
    webhook_requests_handler = SimpleRequestHandler(dispatcher=dp, bot=bot)
    webhook_requests_handler.register(app, path=WEBHOOK_PATH)
    setup_application(app, dp, bot=bot)
    web.run_app(app, host="localhost", port=WEB_SERVER_PORT)


async def main_polling() -> None:
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    if CONNECTION_TYPE == "POLLING":
        asyncio.run(main_polling())
    else:
        main()
