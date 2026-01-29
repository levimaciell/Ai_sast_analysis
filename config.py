from dotenv import load_dotenv
import os

load_dotenv()

class Settings:
    CHAT_GPT_API_KEY = os.getenv("CHAT_GPT_API_KEY")
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    CLAUDE_API_KEY = os.getenv("CLAUDE_API_KEY")
    DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")

settings = Settings()
