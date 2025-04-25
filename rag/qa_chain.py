from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama import OllamaLLM
from config import EMBEDDING_MODEL_NAME

def generate_answer(query, related_docs, chat_history):
    context = "\n\n".join([d.page_content for d in related_docs])

    prompt_template = """
        คุณคือผู้ช่วยอัจฉริยะ ใช้ข้อมูลจาก context และประวัติการพูดคุยเพื่อตอบคำถาม
        กรุณาตอบเป็นภาษาไทย
        Context: {context}
        Chat History: {chat_history}
        Question: {question}
        Answer:
    """

    prompt = ChatPromptTemplate.from_template(prompt_template)
    chain = prompt | OllamaLLM(model=EMBEDDING_MODEL_NAME)

    return chain.invoke({
        "context": context,
        "chat_history": "\n".join(chat_history),
        "question": query
    })
