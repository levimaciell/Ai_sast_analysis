from ai_callers.AiCallerStrategy import AiCallerStrategy
from ai_callers.Structures import AiResults
from anthropic import Anthropic, transform_schema
import json
from config import settings

MODEL = settings.CLAUDE_MODEL
MAX_TOKENS = settings.MAX_TOKENS_CLAUDE
TEMPERATURE = settings.TEMPERATURE
PERSONA = settings.PERSONA

class ClaudeCaller(AiCallerStrategy):

    def __init__(self):
        if not settings.CLAUDE_API_KEY:
            raise ValueError(f"CLAUDE_API_KEY não configurada")

        self.client = Anthropic(api_key=settings.CLAUDE_API_KEY)
    
    def requestAi(self, prompt):
        
        response = self.client.messages.create(
            model= MODEL,
            max_tokens= MAX_TOKENS,
            system=PERSONA,
            messages= [
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            output_config= {
                "format":{
                    "type": "json_schema",
                    "schema": transform_schema(AiResults)
                }
            },
            temperature=TEMPERATURE
        )

        responseList = json.loads(response.content[0].text)

        return responseList['results']
