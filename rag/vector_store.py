from langchain_core.vectorstores import InMemoryVectorStore

def init_vector_store(embeddings):
    return InMemoryVectorStore(embeddings)

def index_documents(store, chunks):
    store.add_documents(chunks)

def search_documents(store, query):
    return store.similarity_search(query)
