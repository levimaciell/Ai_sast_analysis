from dotenv import load_dotenv
import os

load_dotenv()

def _require(value, name):
    if not value:
        raise RuntimeError(f"Missing required env var: {name}")
    return value

class Settings:
    # ========== API KEYS ==========

    CHAT_GPT_API_KEY = _require(os.getenv("CHAT_GPT_API_KEY"), "CHAT_GPT_API_KEY")
    GEMINI_API_KEY = _require(os.getenv("GEMINI_API_KEY"), "GEMINI_API_KEY")
    CLAUDE_API_KEY = _require(os.getenv("CLAUDE_API_KEY"), "CLAUDE_API_KEY")
    DEEPSEEK_API_KEY = _require(os.getenv("DEEPSEEK_API_KEY"), "DEEPSEEK_API_KEY")

    # ========== MODEL NAMES ==========

    CHAT_GPT_MODEL = _require(os.getenv("CHAT_GPT_MODEL"), "CHAT_GPT_MODEL")
    GEMINI_MODEL = _require(os.getenv("GEMINI_MODEL"), "GEMINI_MODEL")
    CLAUDE_MODEL = _require(os.getenv("CLAUDE_MODEL"), "CLAUDE_MODEL")
    DEEPSEEK_MODEL = _require(os.getenv("DEEPSEEK_MODEL"), "DEEPSEEK_MODEL")

    # ========== GENERAL EXPERIMENT CONFIGS ==========

    TEMPERATURE = float(_require(os.getenv("TEMPERATURE"), "TEMPERATURE"))
    MAX_RETRY_ATTEMPTS = int(_require(os.getenv("MAX_RETRY_ATTEMPTS"), "MAX_RETRY_ATTEMPTS"))
    RETRY_DELAY_SECONDS = int(_require(os.getenv("RETRY_DELAY_SECONDS"), "RETRY_DELAY_SECONDS"))

    # ========== OTHER CONFIGS ==========

    MAX_TOKENS_CLAUDE = int(_require(os.getenv("MAX_TOKENS_CLAUDE", "MAX_TOKENS_CLAUDE")))
    BASE_URL_DEEPSEEK = _require(os.getenv("BASE_URL_DEEPSEEK"), "BASE_URL_DEEPSEEK")

    # ========== BASE DIRECTORY ==========
    BASE_DIRECTORY = _require(os.getenv("BASE_DIRECTORY"), "BASE_DIRECTORY")

settings = Settings()
