from contextlib import asynccontextmanager
from aiogram.filters import CommandStart, Command
from fastapi import FastAPI, Request, HTTPException
from aiogram import Bot, Dispatcher, types
from aiogram.types import Update, Message
from loguru import logger
from dotenv import load_dotenv
import os

from frontend_utils import answer_chat

load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')
WEBHOOK_URL = os.getenv('WEBHOOK_URL')
WEBHOOK_PATH = os.getenv('WEBHOOK_PATH')

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

@asynccontextmanager
async def lifespan(app : FastAPI):
    webhook_url = f'{WEBHOOK_URL}{WEBHOOK_PATH}'
    await bot.set_webhook(url=webhook_url,
                           allowed_updates=dp.resolve_used_update_types(),
                           drop_pending_updates=True)
    await bot.send_message(chat_id=741225895, text='Бот запущен')
    logger.info(f'Вебхук установлен {webhook_url}')
    yield
    await bot.send_message(chat_id=741225895, text='Бот остановлен')
    await bot.delete_webhook()
    logger.info(f'Вебхук удален')

app = FastAPI(lifespan=lifespan)

@app.post(WEBHOOK_PATH)
async def webhook_handler(request : Request):
    """
    Обработчик вебхуков
    """
    try:
        update = Update(**await request.json())
        await dp.feed_update(bot, update) # Передача обновления диспетчеру
        return {'status':'ok'}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@dp.message(CommandStart())
async def start_command_handler(message : Message):
    await message.answer(f'Привет, {message.from_user.first_name}! Я работаю на вебхуках.')

@dp.message()
async def echo_answer(message : Message):
    results = await answer_chat(message)
    try:
        # Send a copy of the received message
        await message.answer(results)
    except TypeError:
        # But not all the types is supported to be copied so need to handle it
        await message.answer("Nice try!")



