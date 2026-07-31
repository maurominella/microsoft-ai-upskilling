import os
from dotenv import load_dotenv

def main():
    load_dotenv()
    print(os.environ["AZURE_OPENAI_ENDPOINT"])
    print(os.environ["AZURE_OPENAI_CHAT_DEPLOYMENT_NAME"])
    print("Hello from labs!")


if __name__ == "__main__":
    main()
