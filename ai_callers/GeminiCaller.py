from ai_callers.AiCallerStrategy import AiCallerStrategy
from google import genai
from google.genai import types

MODEL = "gemini-2.5-flash"
TEMPERATURE = 0.0

class GeminiCaller(AiCallerStrategy):

    def __init__(self, api_key):
        self.client = genai.Client(api_key=api_key)
        self.api_key = api_key

    def requestAi(self, prompt):
        response = self.client.models.generate_content(
            model=MODEL,
            contents=prompt,
            config=types.GenerateContentConfig(temperature=TEMPERATURE)
        )

        raw = response.text.strip()

        if raw.startswith("```"):
            raw = raw.replace("```json", "").replace("```", "").strip()

        return raw