from typing import Dict, Any
from fastapi import FastAPI
from loguru import logger
from langchain_community.llms import Ollama
from langchain_core.prompts import PromptTemplate
from langchain.chains import ConversationChain
from langchain.chains.conversation.memory import ConversationBufferMemory
import asyncio
import json
from dotenv import load_dotenv
import os

load_dotenv()

llm_url = os.getenv('LLM_URL')
llm = Ollama(
    model='mistral', 
    base_url=llm_url,
    )

memory = ConversationBufferMemory()
app = FastAPI()

@app.post('/get_answer/')
async def get_answer(item : Dict[str, Any]) -> Dict[str, Any]:
    logger.info(f'В LLM отправлено сообщение {item['text']}')
    template = """Говори на русском языке
    {history}
    Human: {input}
    AI:"""
    prompt = PromptTemplate(
        input_variables=["history", "input"],
        template=template,
    )

    conversation = ConversationChain(
        llm=llm,
        memory=memory,
        prompt=prompt,
        verbose=True,
    )

    output = conversation.invoke({'input': item['text']})
    return {'text': output['response']}
