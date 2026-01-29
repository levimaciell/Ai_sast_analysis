from ai_callers.AiCallerStrategy import AiCallerStrategy
from ai_callers.Structures import AiResults
from openai import OpenAI
from config import settings
import json

TEMPERATURE=0.0
MODEL="gpt-5.2"

class ChatGptCaller(AiCallerStrategy):

    def __init__(self):
        if not settings.CHAT_GPT_API_KEY:
            raise ValueError(f"CHAT_GPT_API_KEY não configurada") 
        
        self.client = OpenAI(api_key=settings.CHAT_GPT_API_KEY)

    def requestAi(self, prompt):

        response = self.client.responses.parse(
            model=MODEL,
            input=prompt,
            temperature=TEMPERATURE,
            text_format=AiResults
        )

        resultsList = json.loads(response.output_text)
        
        return resultsList['results']
