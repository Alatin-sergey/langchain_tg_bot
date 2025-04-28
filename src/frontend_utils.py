from aiogram.types import Message
from aiohttp import ClientSession, ClientTimeout
import asyncio
from loguru import logger
from dotenv import load_dotenv
import os
import json

load_dotenv()

async def answer_chat(massage : Message) -> str:
    text = massage.text
    logger.info(f'text: {text}')
    async with ClientSession() as session:
        url = os.getenv('BACKEND_ENDPOINT')
        data = {'text' : text}
        try:
            async with session.post(url=url, json=data) as response:
                response.raise_for_status()
                response_data = await response.json()
                logger.info(f'From LLM: {response_data}')
                return response_data['text']
        except Exception:
            return 'Error'
            


