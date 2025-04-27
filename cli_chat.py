import os
import re
from rag import loader, splitter, embedding, vector_store, qa_chain

def clean_text(text):
    return re.sub(r'[^\x00-\x7Fก-๙เ-์ ]+', '', text)

def run_cli():
    while True:
        try:
            print("\nPlease enter the path to your PDF file (type 'menu' to return to the main menu).")
            pdf_path = input("Path: ").strip()

            if pdf_path.lower() == "menu":
                return

            if not os.path.exists(pdf_path):
                print("File not found. Please try again.")
                continue

            docs = loader.load_pdf(pdf_path)
            chunks = splitter.split_documents(docs)
            embeds = embedding.get_embeddings()
            store = vector_store.init_vector_store(embeds, chunks)

            print("\nPDF loaded and processed successfully. You can now start asking questions.")

            chat_history = []

            while True:
                query = input("\nEnter your question (type 'exit' to quit, 'menu' to return to main menu): ").strip()

                if query.lower() == "exit":
                    print("Goodbye!")
                    exit(0)
                if query.lower() == "menu":
                    return

                query_clean = clean_text(query)
                related_docs = vector_store.search_documents(store, query_clean, top_k=4)
                answer = qa_chain.generate_answer(query_clean, related_docs, chat_history)

                chat_history.append(f"User: {query}")
                chat_history.append(f"Bot: {answer}")

                print(f"\nAnswer: {answer}\n")

        except KeyboardInterrupt:
            print("\nGoodbye!")
            exit(0)