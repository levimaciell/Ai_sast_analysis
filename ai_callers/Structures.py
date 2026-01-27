from pydantic import BaseModel, Field
from typing import List

class Label(BaseModel):
    label: str = Field(description="String no formato CWE-XXX")
    line_of_code: int = Field(description="Linha de código onde foi encontrada a vulnerabilidade")

class AiResults(BaseModel):
    results: List[Label] = Field(description="Retorna uma lista contendo vários AiResult")