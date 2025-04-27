# rag/qa_chain.py
import re
from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama import OllamaLLM
from config import EMBEDDING_MODEL_NAME

def clean_text(text):
    return re.sub(r'[^\x00-\x7Fก-๙เ-์ ]+', '', text)

def generate_answer(query, related_docs, chat_history):
    context = "\n\n".join([clean_text(d.page_content[:700]) for d in related_docs])
    chat_history_str = "\n".join(clean_text(m) for m in chat_history)

    prompt_template = """
        Answer the user's question based on the provided context and chat history.
        
        Context:
        {context}
        
        Chat History:
        {chat_history}
        
        Question:
        {question}
        
        Answer:
    """

    prompt = ChatPromptTemplate.from_template(prompt_template)
    chain = prompt | OllamaLLM(model=EMBEDDING_MODEL_NAME)

    return chain.invoke({
        "context": context,
        "chat_history": chat_history_str,
        "question": clean_text(query)
    })