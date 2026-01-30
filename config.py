from dotenv import load_dotenv
import os

load_dotenv()

def _require(value, name):
    if not value:
        raise RuntimeError(f"Missing required env var: {name}")
    return value

def _require_float(value, name):
    value = _require(value, name)
    try:
        return float(value)
    except ValueError:
        raise RuntimeError(f"Invalid float value for {name}: {value}")
    
def _require_int(value, name):
    value = _require(value, name)
    try:
        return int(value)
    except ValueError:
        raise RuntimeError(f"Invalid int value for {name}: {value}")

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

    TEMPERATURE = float(_require_float(os.getenv("TEMPERATURE"), "TEMPERATURE"))
    MAX_RETRY_ATTEMPTS = int(_require_int(os.getenv("MAX_RETRY_ATTEMPTS"), "MAX_RETRY_ATTEMPTS"))
    RETRY_DELAY_SECONDS = int(_require_int(os.getenv("RETRY_DELAY_SECONDS"), "RETRY_DELAY_SECONDS"))

    # ========== OTHER CONFIGS ==========

    MAX_TOKENS_CLAUDE = int(_require_int(os.getenv("MAX_TOKENS_CLAUDE"), "MAX_TOKENS_CLAUDE"))
    BASE_URL_DEEPSEEK = _require(os.getenv("BASE_URL_DEEPSEEK"), "BASE_URL_DEEPSEEK")
    SAST_TO_RUN = _require(os.getenv("SAST_TO_RUN"), "SAST_TO_RUN")

    # ========== BASE DIRECTORY ==========
    BASE_DIRECTORY = _require(os.getenv("BASE_DIRECTORY"), "BASE_DIRECTORY")

    def validate(self):
        required_vars = {
            "CHAT_GPT_API_KEY": self.CHAT_GPT_API_KEY,
            "GEMINI_API_KEY": self.GEMINI_API_KEY,
            "CLAUDE_API_KEY": self.CLAUDE_API_KEY,
            "DEEPSEEK_API_KEY": self.DEEPSEEK_API_KEY,

            "CHAT_GPT_MODEL": self.CHAT_GPT_MODEL,
            "GEMINI_MODEL": self.GEMINI_MODEL,
            "CLAUDE_MODEL": self.CLAUDE_MODEL,
            "DEEPSEEK_MODEL": self.DEEPSEEK_MODEL,

            "TEMPERATURE": self.TEMPERATURE,
            "MAX_RETRY_ATTEMPTS": self.MAX_RETRY_ATTEMPTS,
            "RETRY_DELAY_SECONDS": self.RETRY_DELAY_SECONDS,

            "MAX_TOKENS_CLAUDE": self.MAX_TOKENS_CLAUDE,
            "BASE_URL_DEEPSEEK": self.BASE_URL_DEEPSEEK,
            "BASE_DIRECTORY": self.BASE_DIRECTORY,
        }

        missing = [
            name for name, value in required_vars.items()
            if value is None or (isinstance(value, str) and value.strip() == "")
        ]

        if missing:
            raise RuntimeError(
                "Missing required environment variables:\n - "
                + "\n - ".join(missing)
            )

settings = Settings()
