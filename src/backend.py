from contextlib import asynccontextmanager
from fastapi import FastAPI
from pydantic import BaseModel
from loguru import logger
from langchain_community.llms import Ollama
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.prompts import PromptTemplate, ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate
from langchain.chains import LLMChain, ConversationChain
from langchain.chains.conversation.memory import ConversationBufferMemory
import asyncio
import json

OLLAMA_URL = "http://localhost:11434"

llm = Ollama(model="mistral")

memory = ConversationBufferMemory()

class Item(BaseModel):
    text : str

@asynccontextmanager
async def lifespan(app : FastAPI):
    logger.info(f'Связь с LLM установлена {OLLAMA_URL}')
    yield
    logger.info(f'Работа с LLM завершена')

app = FastAPI()

@app.post('/get_answer/')
async def get_answer(item: Item) -> dict:
    messege_from_user = item.text
    logger.info(f'В LLM отправлено сообщение {messege_from_user}')


    
    template = """Говори на русском языке
    
    {history}
    Human: {input}
    AI:"""

    prompt = PromptTemplate(
        input_variables=["history", "input"],
        template=template
    )

    conversation = ConversationChain(
        llm=llm,
        memory=memory,
        prompt=prompt,
        verbose=True
    )
    
    #output = llm.invoke(prompt)

    output = conversation.invoke({'input': messege_from_user})
    logger.info(f'LLM вернула сообщение {output['response']}')
    logger.info(f'В памяти находится: {conversation.memory.buffer}')


    return {'text': output['response']}
