from langchain_ollama import ChatOllama
from langchain_core.language_models.chat_models import BaseChatModel

def get_llm(model_name: str = "qwen2.5:0.5b") -> BaseChatModel:
    """
    Returns an instance of the local LLM. 
    By default, expects an Ollama server running on ollama:11434.
    The default model is qwen2.5:0.5b as it supports tool calling.
    """
    return ChatOllama(
        model=model_name,
        base_url="http://ollama:11434",
        temperature=0.1,
    )
