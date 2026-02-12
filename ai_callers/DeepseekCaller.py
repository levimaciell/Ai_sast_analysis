from ai_callers.AiCallerStrategy import AiCallerStrategy
from openai import OpenAI
import json
from config import settings

BASE_URL = settings.BASE_URL_DEEPSEEK
MODEL = settings.DEEPSEEK_MODEL
TEMPERATURE = settings.TEMPERATURE
PERSONA = settings.PERSONA

class DeepseekCaller(AiCallerStrategy):

    def __init__(self):
        if not settings.DEEPSEEK_API_KEY:
            raise ValueError(f"DEEPSEEK_API_KEY não configurada")

        self.client = OpenAI(api_key=settings.DEEPSEEK_API_KEY, base_url=BASE_URL)

    def requestAi(self, prompt):

        response = self.client.chat.completions.create(
            model=MODEL,
            messages=[
                {"role": "system", "content": PERSONA},
                {"role": "user", "content": prompt}
            ],
            response_format={'type':'json_object'},
            temperature=TEMPERATURE,
            stream=False
        )

        raw = response.choices[0].message.content.strip()
        resultsList = json.loads(raw)

        return resultsList