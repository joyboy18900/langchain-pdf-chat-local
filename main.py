import sys

def main():
    if len(sys.argv) > 1:
        mode = sys.argv[1]
        if mode == '--mode' and len(sys.argv) > 2:
            if sys.argv[2] == 'cli':
                from cli_chat import run_cli
                run_cli()
                return
            else:
                print("Unknown mode. Please use 'cli'.")
                return

    # ถ้าไม่ใส่ argument → เข้า CLI ทันที
    from cli_chat import run_cli
    run_cli()

if __name__ == "__main__":
    main()

# import os
# import sys
#
# def main():
#     if len(sys.argv) > 1:
#         mode = sys.argv[1]
#         if mode == '--mode' and len(sys.argv) > 2:
#             if sys.argv[2] == 'cli':
#                 from cli_chat import run_cli
#                 run_cli()
#                 return
#             elif sys.argv[2] == 'ui':
#                 print("\nStarting Streamlit UI...")
#                 os.system("streamlit run ui_chat.py")
#                 return
#             else:
#                 print("Unknown mode. Please use 'cli' or 'ui'.")
#                 return
#
#     # No arguments, show interactive menu
#     while True:
#         print("\nWelcome to the LangChain Thai PDF RAG Assistant")
#         print("Select an option:")
#         print("1. Run as CLI (Command Line Chatbot)")
#         print("2. Run as UI (Streamlit Web App)")
#         print("3. Exit")
#
#         choice = input("Enter your choice (1, 2, or 3): ").strip()
#
#         if choice == '1':
#             from cli_chat import run_cli
#             run_cli()
#         elif choice == '2':
#             print("\nStarting Streamlit UI...")
#             os.system("streamlit run ui_chat.py")
#             break
#         elif choice == '3':
#             print("Goodbye!")
#             break
#         else:
#             print("Invalid choice. Please try again.")
#
# if __name__ == "__main__":
#     main()