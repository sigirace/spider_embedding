from pydantic import BaseModel
from llm.domain.model.llm_schema import Message
from typing import List


class ChatRequest(BaseModel):
    messages: List[Message]


class ChatResponse(BaseModel):
    content: str
