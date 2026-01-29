from ai_callers.AiCallerStrategy import AiCallerStrategy
from openai import OpenAI
import json
from config import settings

BASE_URL = 'https://api.deepseek.com'
MODEL = 'deepseek-chat'
TEMPERATURE = 0.0
EXAMPLE_JSON = '''
[
    {
        "label": "CWE-78",
        "line_of_code": 15
    },
    {
        "label": "CWE-94",
        "line_of_code": 35
    }
]
'''

class DeepseekCaller(AiCallerStrategy):

    def __init__(self):
        if not settings.DEEPSEEK_API_KEY:
            raise ValueError(f"DEEPSEEK_API_KEY não configurada")

        self.client = OpenAI(api_key=settings.DEEPSEEK_API_KEY, base_url=BASE_URL)

    def requestAi(self, prompt):

        modifiedPrompt = f'{prompt}\n Example Json: \n {EXAMPLE_JSON}'

        response = self.client.chat.completions.create(
            model=MODEL,
            messages=[
                {"role": "user", "content": modifiedPrompt}
            ],
            response_format={'type':'json_object'},
            temperature=TEMPERATURE,
            stream=False
        )

        raw = response.choices[0].message.content.strip()
        resultsList = json.loads(raw)

        return resultsList