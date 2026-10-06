from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    user_id: str = Field(min_length=1, max_length=100)
    message: str = Field(min_length=1, max_length=5000)


class ChatResponse(BaseModel):
    answer: str
    intent: str
    citations: list[str]
    security_flags: list[str]
    activity_log: list[dict]
    analysis: dict