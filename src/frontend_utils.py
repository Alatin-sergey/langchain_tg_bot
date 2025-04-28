from aiogram.types import Message
from aiohttp import ClientSession, ClientTimeout
import asyncio
from dotenv import load_dotenv
import os
import json

load_dotenv()

async def answer_chat(massage : Message):
    text = massage.text
    #print(type(massage))
    #print(massage.text)


    async with ClientSession() as session:
        url = os.getenv('BACKEND_ENDPOINT')
        data = {'text' : text}
        #print(f'url: {url}')
        #print(f'data: {data}')

        async with session.post(url=url, json=data) as response:
            #print(f'response.status: {response.status}')
            #print('type response: \n', type(response))
            #print('response.__dict__ \n', response.__dict__)
            #print('session.__methods__\n', session.__methods__)
            try:
                if response.status == 200:
                    response_data = await response.json()
                    return response_data['text']
                else:
                    raise Exception('Ошибка, response.status != 200')
            except:
                return 'Error'
            


