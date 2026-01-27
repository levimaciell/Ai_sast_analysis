from ai_callers.AiCallerStrategy import AiCallerStrategy
from pydantic import BaseModel, Field, RootModel
from openai import OpenAI

TEMPERATURE=0.0
MODEL="gpt-5.2"

class ChatGptCaller(AiCallerStrategy):

    def __init__(self, api_key):
        self.client = OpenAI(api_key=api_key)
        self.api_key = api_key

    def requestAi(self, prompt):

        response = self.client.responses.create(
            model=MODEL,
            input=prompt,
            temperature=TEMPERATURE
        )

        return response.output_text
