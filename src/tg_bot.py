from aiogram.filters import CommandStart
from aiohttp import web

from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application
from loguru import logger
from aiogram import Bot, Dispatcher, Router
from aiogram.types import Message
from dotenv import load_dotenv
import os

from frontend_utils import answer_chat

load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')
WEB_SERVER_HOST = os.getenv("WEB_SERVER_HOST")
WEB_SERVER_PORT = int(os.getenv("WEB_SERVER_PORT"))
WEBHOOK_PATH = os.getenv('WEBHOOK_PATH')
WEBHOOK_URL = os.getenv('WEBHOOK_URL')

router = Router()

bot = Bot(token=BOT_TOKEN)

async def on_startup(bot: Bot) -> None:
    webhook_url = f'{WEBHOOK_URL}{WEBHOOK_PATH}'
    await bot.set_webhook(url=webhook_url,
                           allowed_updates=router.resolve_used_update_types(),
                           drop_pending_updates=True)

@router.message(CommandStart())
async def start_command_handler(message : Message) -> None:
    await message.answer(f'Привет, {message.from_user.first_name}! Я работаю на вебхуках.')

@router.message()
async def echo_answer(message : Message) -> None:
    results = await answer_chat(message)
    try:
        await message.answer(results)
    except TypeError:
        await message.answer("Nice try!")

def main() -> None:
    dp = Dispatcher()
    dp.include_router(router)
    dp.startup.register(on_startup)
    app = web.Application()
    webhook_requests_handler = SimpleRequestHandler(dispatcher=dp, bot=bot)
    webhook_requests_handler.register(app, path=WEBHOOK_PATH)
    setup_application(app, dp, bot=bot)
    web.run_app(app, host='localhost', port=WEB_SERVER_PORT)

if __name__ == "__main__":
    main()