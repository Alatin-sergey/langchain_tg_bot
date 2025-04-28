from typing import Dict, Any
from fastapi import FastAPI
from dotenv import load_dotenv
import os
from chat_backend import Local_LLM
import uvicorn

load_dotenv()

model = Local_LLM(model="mistral", base_url=os.getenv("LLM_URL"))

app = FastAPI()


@app.post("/get_answer/")
async def get_answer(item: Dict[str, Any]) -> Dict[str, Any]:
    return {"text": model.generate(input=item["text"])}


if __name__ == "__main__":
    uvicorn.run(
        "backend:app", 
        host=os.getenv("BACKEND_HOST"), 
        port=int(os.getenv("BACKEND_PORT")),
)
