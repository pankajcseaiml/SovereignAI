from langchain_ollama import OllamaEmbeddings
from langchain_core.embeddings import Embeddings

def get_embeddings(model_name: str = "nomic-embed-text") -> Embeddings:
    """
    Returns an instance of local embeddings using Ollama.
    The default model is 'nomic-embed-text' which is highly capable for RAG.
    Expects an Ollama server running on localhost:11434.
    """
    return OllamaEmbeddings(
        model=model_name,
        base_url="http://ollama:11434",
    )
