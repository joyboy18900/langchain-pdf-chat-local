import os
import streamlit as st
from config import PDF_DIRECTORY
from rag import loader, splitter, embedding, vector_store, qa_chain

# Setup
os.makedirs(PDF_DIRECTORY, exist_ok=True)
st.title("💬 Thai PDF Chatbot (LLaMA 3)")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

uploaded_file = st.file_uploader("📄 Upload PDF", type=["pdf"])
if uploaded_file:
    file_path = os.path.join(PDF_DIRECTORY, uploaded_file.name)
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    docs = loader.load_pdf(file_path)
    chunks = splitter.split_documents(docs)

    embeddings = embedding.get_embeddings()
    store = vector_store.init_vector_store(embeddings)
    vector_store.index_documents(store, chunks)

    st.success("✅ เอกสารถูกจัดการเรียบร้อย!")

    query = st.text_input("ถามคำถามของคุณ:")
    if query:
        with st.spinner("💭 คิดคำตอบ..."):
            related = vector_store.search_documents(store, query)
            answer = qa_chain.generate_answer(query, related, st.session_state.chat_history)
            st.session_state.chat_history.append(f"User: {query}")
            st.session_state.chat_history.append(f"Bot: {answer}")
        for msg in st.session_state.chat_history:
            st.write(msg)