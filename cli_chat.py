import sys
import re
from rag import loader, splitter, embedding, vector_store, qa_chain
from config import EMBEDDING_MODEL_NAME

def clean_text(text):
    return re.sub(r'[^\x00-\x7Fก-๙เ-์ ]+', '', text)

def main(pdf_path):
    # Load and split document
    docs = loader.load_pdf(pdf_path)
    chunks = splitter.split_documents(docs)

    # Create embedding and vector store (FAISS)
    embeds = embedding.get_embeddings()
    store = vector_store.init_vector_store(embeds, chunks)

    print("\n✅ PDF ประมวลผลเรียบร้อย พร้อมถามคำถามแล้ว\n")

    # Start chat loop
    chat_history = []
    while True:
        try:
            query = input("❓ ถามคำถาม (หรือพิมพ์ 'exit' เพื่อออก): ").strip()
            if query.lower() == 'exit':
                print("👋 ลาก่อน!")
                break

            # Clean input
            query_clean = clean_text(query)

            # Search relevant documents
            related_docs = vector_store.search_documents(store, query_clean, top_k=4)

            # Generate answer
            answer = qa_chain.generate_answer(query_clean, related_docs, chat_history)

            # Append and show
            chat_history.append(f"User: {query}")
            chat_history.append(f"Bot: {answer}")
            print(f"\n🤖 {answer}\n")

        except KeyboardInterrupt:
            print("\n👋 ลาก่อน!")
            break


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python cli_chat.py <path_to_pdf>")
    else:
        main(sys.argv[1])
