from langchain_ollama import OllamaEmbeddings
from config import EMBEDDING_MODEL_NAME

def get_embeddings():
    return OllamaEmbeddings(model=EMBEDDING_MODEL_NAME)
