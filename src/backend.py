from typing import Dict, Any
from fastapi import FastAPI
from loguru import logger
from dotenv import load_dotenv
import os
from chat_backend import Local_LLM
import uvicorn

load_dotenv()

model = Local_LLM(model='mistral', base_url=os.getenv('LLM_URL'))

app = FastAPI()


@app.post('/get_answer/')
async def get_answer(item : Dict[str, Any]) -> Dict[str, Any]:
    logger.info(f'В LLM отправлено сообщение {item['text']}')
    return {'text': model.generate(input = item['text'])}

if __name__ == "__main__":
    uvicorn.run("backend:app", host='0.0.0.0', port=8001)
