# import os
# import streamlit as st
# from rag import loader, splitter, embedding, vector_store, qa_chain
# from config import PDF_DIRECTORY
#
# st.title("LangChain PDF Chatbot - UI Version")
# os.makedirs(PDF_DIRECTORY, exist_ok=True)
#
# if "chat_history" not in st.session_state:
#     st.session_state.chat_history = []
#
# uploaded_file = st.file_uploader("Upload your PDF file", type=["pdf"])
#
# if uploaded_file and "vector_store" not in st.session_state:
#     file_path = os.path.join(PDF_DIRECTORY, uploaded_file.name)
#
#     with open(file_path, "wb") as f:
#         f.write(uploaded_file.getbuffer())
#
#     if os.path.exists(file_path):
#         docs = loader.load_pdf(file_path)
#
#         if not docs:
#             st.error(
#                 "The uploaded PDF could not be processed. It may be empty or image-based without extractable text.")
#         else:
#             chunks = splitter.split_documents(docs)
#
#             if not chunks:
#                 st.error("Failed to split the document into chunks.")
#             else:
#                 # ใช้ embeddings model ไม่ใช่ผลลัพธ์
#                 embeds_model = embedding.get_embeddings()
#                 store = vector_store.init_vector_store(embeds_model, chunks)
#                 st.session_state.vector_store = store
#                 st.success("PDF loaded and processed successfully.")
#     else:
#         st.error("Failed to save the uploaded file. Please try again.")
#
# query = st.text_input("Enter your question:")
#
# if query and "vector_store" in st.session_state:
#     with st.spinner("Generating answer..."):
#         store = st.session_state.vector_store
#         related_docs = vector_store.search_documents(store, query, top_k=4)
#         answer = qa_chain.generate_answer(query, related_docs, st.session_state.chat_history)
#
#         st.session_state.chat_history.append(f"User: {query}")
#         st.session_state.chat_history.append(f"Bot: {answer}")
#
#     for msg in st.session_state.chat_history:
#         st.write(msg)