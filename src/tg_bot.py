from aiogram.filters import CommandStart
from aiohttp import web, ClientSession
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application
from loguru import logger
from aiogram import Bot, Dispatcher, Router
from aiogram.types import Message
from dotenv import load_dotenv
import os

load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')
WEB_SERVER_HOST = os.getenv("WEB_SERVER_HOST")
WEB_SERVER_PORT = int(os.getenv("WEB_SERVER_PORT"))
WEBHOOK_PATH = os.getenv('WEBHOOK_PATH')
WEBHOOK_URL = os.getenv('WEBHOOK_URL')
BACKEND_ENDPOINT = os.getenv('BACKEND_ENDPOINT')

router = Router()
bot = Bot(token=BOT_TOKEN)

async def on_startup(bot: Bot) -> None:
    await bot.set_webhook(
        url=f'{WEBHOOK_URL}{WEBHOOK_PATH}',
        allowed_updates=router.resolve_used_update_types(),
        drop_pending_updates=True,
        )


@router.message(CommandStart())
async def start_command_handler(message : Message) -> None:
    await message.answer(f'Привет, {message.from_user.first_name}! Я работаю на вебхуках.')


@router.message()
async def echo_answer(massege : Message) -> None:
    data = {'text' : massege.text}
    async with ClientSession().post(url=BACKEND_ENDPOINT, json=data) as response:
        try:
            response.raise_for_status()
            response_data = await response.json()
            logger.info(f'From LLM: {response_data}')
            answer = response_data['text']
        except Exception:
            answer = response_data['text']
        response.close()
    await massege.answer(answer) 



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