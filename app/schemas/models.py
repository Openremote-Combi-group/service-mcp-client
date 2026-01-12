from pydantic import BaseModel


class AIModel(BaseModel):
    name: str
    provider: str

