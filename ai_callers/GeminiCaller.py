from ai_callers.AiCallerStrategy import AiCallerStrategy
from ai_callers.Structures import AiResults
from google import genai
import json
from config import settings

MODEL = "gemini-2.5-flash"
TEMPERATURE = 0.0

class GeminiCaller(AiCallerStrategy):

    def __init__(self):
        if not settings.GEMINI_API_KEY:
            raise ValueError(f"GEMINI_API_KEY não configurada")

        self.client = genai.Client(api_key=settings.GEMINI_API_KEY)

    def requestAi(self, prompt):

        response = self.client.models.generate_content(
            model=MODEL,
            contents=prompt,
            config={
                'temperature': TEMPERATURE,
                'response_mime_type': 'application/json',
                'response_json_schema': AiResults.model_json_schema()
            }
        )

        raw = response.text.strip()
        resultsList = json.loads(raw)

        return resultsList['results']