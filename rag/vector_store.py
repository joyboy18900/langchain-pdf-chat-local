from langchain_community.vectorstores import FAISS

def init_vector_store(embeddings, chunks):
    return FAISS.from_documents(chunks, embedding=embeddings)

def search_documents(store, query, top_k=4):
    return store.similarity_search(query, k=top_k)