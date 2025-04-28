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
        
        self.memory = ConversationBufferMemory()

    def generate(self,  input : str):
        template = """Говори на русском языке.
        {history}
        Human: {input}
        AI:"""
        prompt_template = PromptTemplate(
        input_variables=["history", "input"],
        template=template,
        )

        conversation = ConversationChain(
        llm=self.llm,
        memory=self.memory,
        prompt=prompt_template,
        verbose=True,
        )

        return conversation.invoke({"input": input})['response']



        

