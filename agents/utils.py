
from langchain.chat_models import ChatGroq
from langchain.prompts import ChatPromptTemplate
from langchain.schema import SystemMessage, HumanMessage

def create_llm(config):
    """Creates and returns a ChatGroq LLM."""
    return ChatGroq(
        temperature=0.7,
        model_name=config["model_name"],
        groq_api_key=config["groq_api_key"]
    )

def create_prompt(instructions):
    return ChatPromptTemplate.from_messages([
        SystemMessage(content=instructions),
        HumanMessage(content="{input}")
    ])



