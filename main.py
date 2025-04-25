# from langchain_ollama import OllamaEmbeddings, OllamaLLM
# from langchain_community.document_loaders import PDFPlumberLoader
# from langchain_text_splitters import RecursiveCharacterTextSplitter
# from langchain_core.vectorstores import InMemoryVectorStore
# from langchain_core.prompts import ChatPromptTemplate
# import os
# import streamlit as st
#
#
# # Create directory for PDF storage if it doesn't exist
# PDF_DIRECTORY = "documents/pdfs/"
# os.makedirs(PDF_DIRECTORY, exist_ok=True)
#
# # Model configuration
# # EMBEDDING_MODEL_NAME = "deepseek-r1:1.5b"
# EMBEDDING_MODEL_NAME = "llama3:8b-instruct-fp16"
#
# # Initialize embeddings and vector store
# embeddings = OllamaEmbeddings(model=EMBEDDING_MODEL_NAME)
# vector_db = InMemoryVectorStore(embeddings)
#
# # Initialize LLM
# llm = OllamaLLM(model=EMBEDDING_MODEL_NAME)
#
# # Helper functions
# def save_uploaded_file(uploaded_file):
#     file_path = PDF_DIRECTORY + uploaded_file.name
#     with open(file_path, "wb") as f:
#         f.write(uploaded_file.getbuffer())
#     return file_path
#
# def load_pdf(file_path):
#     loader = PDFPlumberLoader(file_path)
#     return loader.load()
#
# def split_into_chunks(docs):
#     splitter = RecursiveCharacterTextSplitter(
#         chunk_size=1000,
#         chunk_overlap=200
#     )
#     return splitter.split_documents(docs)
#
# def index_chunks(chunks):
#     vector_db.add_documents(chunks)
#
# def find_related_docs(query):
#     return vector_db.similarity_search(query)
#
# def generate_answer(user_query, related_docs, chat_history):
#     context = "\n\n".join([d.page_content for d in related_docs])
#
#     # prompt_template = """
#     #     You are a smart assistant. Use the context below and chat history to answer user's question.
#     #     Context: {context}
#     #     Chat History: {chat_history}
#     #     Question: {question}
#     #     Answer:
#     # """
#
#     prompt_template = """
#         คุณเป็นผู้ช่วยอัจฉริยะ ให้ใช้ข้อมูลจาก context และประวัติการพูดคุยด้านล่างเพื่อตอบคำถามของผู้ใช้เป็น **ภาษาไทย** เท่านั้น
#         Context: {context}
#         Chat History: {chat_history}
#         Question: {question}
#         Answer (ตอบเป็นภาษาไทย):
#     """
#
#     chat_prompt = ChatPromptTemplate.from_template(prompt_template)
#     chain = chat_prompt | llm
#
#     final_answer = chain.invoke({
#         "context": context,
#         "chat_history": "\n".join(chat_history),
#         "question": user_query
#     })
#
#     return final_answer
#
#
# # Streamlit UI
# st.title("DeepSeek RAG Chat")
# st.write("Ask questions about your PDF using DeepSeek-R1 and Ollama!")
#
# # Session state for chat history
# if "chat_history" not in st.session_state:
#     st.session_state.chat_history = []
#
# # File upload
# uploaded_file = st.file_uploader("Upload PDF", type=["pdf"])
#
# if uploaded_file is not None:
#     # 1. Save the file
#     path_to_pdf = save_uploaded_file(uploaded_file)
#
#     # 2. Load the PDF content
#     docs = load_pdf(path_to_pdf)
#
#     # 3. Split into chunks
#     chunks = split_into_chunks(docs)
#
#     # 4. Index chunks in the vector store
#     index_chunks(chunks)
#
#     st.success("PDF indexed successfully! Type your questions below.")
#
#     # Chat interaction
#     user_query = st.text_input("Ask a question")
#
#     if user_query:
#         with st.spinner("Searching and generating answer..."):
#             # 5. Find the relevant chunks
#             related_docs = find_related_docs(user_query)
#
#             # 6. Generate the final answer
#             answer = generate_answer(user_query, related_docs, st.session_state.chat_history)
#
#             # Append to chat history
#             st.session_state.chat_history.append(f"User: {user_query}")
#             st.session_state.chat_history.append(f"Assistant: {answer}")
#
#         # Display chat history
#         for message in st.session_state.chat_history:
#             st.write(message)
#
# if not uploaded_file:
#     st.info("Please upload a PDF file to get started.")