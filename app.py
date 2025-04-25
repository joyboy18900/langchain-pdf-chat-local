import os
import streamlit as st
from config import PDF_DIRECTORY
from rag import loader, splitter, embedding, vector_store, qa_chain

st.title("📄 Thai PDF Chatbot (LLaMA 3)")
os.makedirs(PDF_DIRECTORY, exist_ok=True)

# Init session state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

uploaded_file = st.file_uploader("📂 Upload PDF", type=["pdf"])

if uploaded_file and "vector_store" not in st.session_state:
    # Save file
    file_path = os.path.join(PDF_DIRECTORY, uploaded_file.name)
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    # Load & preprocess
    docs = loader.load_pdf(file_path)
    chunks = splitter.split_documents(docs)
    embeds = embedding.get_embeddings()

    # FAISS index
    store = vector_store.init_vector_store(embeds, chunks)
    st.session_state.vector_store = store
    st.success("✅ PDF Indexed with FAISS!")

query = st.text_input("❓ ถามอะไรเกี่ยวกับเอกสาร:")

if query and "vector_store" in st.session_state:
    with st.spinner("🤖 คิดคำตอบ..."):
        store = st.session_state.vector_store
        related_docs = vector_store.search_documents(store, query, top_k=4)
        answer = qa_chain.generate_answer(query, related_docs, st.session_state.chat_history)

        st.session_state.chat_history.append(f"User: {query}")
        st.session_state.chat_history.append(f"Bot: {answer}")

    for msg in st.session_state.chat_history:
        st.write(msg)