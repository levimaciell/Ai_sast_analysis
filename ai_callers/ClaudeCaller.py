from ai_callers.AiCallerStrategy import AiCallerStrategy
from ai_callers.Structures import AiResults
from anthropic import Anthropic
import json
from config import settings

MODEL = 'claude-haiku-4-5'
MAX_TOKENS = 300
BETA_LIST = ["structured-outputs-2025-11-13"]
TEMPERATURE = 0.0


class ClaudeCaller(AiCallerStrategy):

    def __init__(self):
        if not settings.CLAUDE_API_KEY:
            raise ValueError(f"CLAUDE_API_KEY não configurada")

        self.client = Anthropic(api_key=settings.CLAUDE_API_KEY)
    
    def requestAi(self, prompt):
        
        response = self.client.beta.messages.parse(
            model= MODEL,
            max_tokens= MAX_TOKENS,
            betas=BETA_LIST,
            messages= [
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            output_format = AiResults,
            temperature=TEMPERATURE
        )

        responseList = json.loads(response.parsed_output.model_dump_json())
        return responseList['results']


# r = self.client.messages.count_tokens(
#             model= MODEL,
#             messages=[{
#                 "role": "user",
#                 "content": prompt
#             }]
#         )
