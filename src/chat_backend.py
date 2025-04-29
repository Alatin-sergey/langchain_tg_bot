from abc import ABC
from langchain_community.llms import Ollama
from langchain_core.prompts import PromptTemplate
from langchain.chains import ConversationChain
from langchain.chains.conversation.memory import ConversationBufferMemory


class BaseModel(ABC):
    ...


class Local_LLM(BaseModel):
    def __init__(self, model, base_url):
        self.llm = Ollama(
            model=model, 
            base_url=base_url,
        )
        
        self.template = """Говори на русском языке.
            {history}
            Human: {input}
            AI:"""

        self.prompt_template = PromptTemplate(
            input_variables=["history", "input"],
            template=self.template,
        )
        
        self.memory = ConversationBufferMemory()


    def generate(self,  input: str) -> str:
        conversation = ConversationChain(
            llm=self.llm,
            memory=self.memory,
            prompt=self.prompt_template,
            verbose=True,
        )

        return conversation.invoke({"input": input})["response"]
