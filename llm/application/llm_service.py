from typing import AsyncGenerator, Generator, List
from llm.domain.model.llm_schema import Message
from llm.domain.repository.llm_repository import ILLMRepository


class LLMService:
    """Encapsulates business rules; can add logging, retries, etc."""

    def __init__(self, llm_repository: ILLMRepository):
        self.llm_repository = llm_repository

    # fully synchronous use‑case
    def chat(self, messages: List[Message]) -> str:
        return self.llm_repository.invoke(messages)

    # fully asynchronous
    async def chat_async(self, messages: List[Message]) -> str:
        return await self.llm_repository.ainvoke(messages)

    # streaming helpers
    def chat_stream(self, messages: List[Message]) -> Generator[str, None, None]:
        return self.llm_repository.stream(messages)

    async def chat_astream(self, messages: List[Message]) -> AsyncGenerator[str, None]:
        async for chunk in self.llm_repository.astream(messages):
            yield chunk
