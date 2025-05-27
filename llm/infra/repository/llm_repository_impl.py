from typing import AsyncGenerator, Generator, List
from llm.domain.model.llm_schema import Message
from llm.domain.repository.llm_repository import ILLMRepository
from llm.infra.api.haiqv_chat_ollama import ollama_client


class HaiqvLLMRepository(ILLMRepository):
    """Concrete adapter that talks to HaiQV‑proxied Ollama."""

    def _to_langchain(self, messages: List[Message]):
        # LangChain expects dict‑style messages
        return [{"role": m.role.value, "content": m.content} for m in messages]

    # blocking
    def invoke(self, messages: List[Message]) -> str:
        return ollama_client.invoke(self._to_langchain(messages))

    # async
    async def ainvoke(self, messages: List[Message]) -> str:
        return await ollama_client.ainvoke(self._to_langchain(messages))

    # sync stream (generator of tokens / chunks)
    def stream(self, messages: List[Message]):
        for chunk in ollama_client.stream(self._to_langchain(messages)):
            yield chunk

    # async stream
    async def astream(self, messages: List[Message]):
        async for chunk in ollama_client.astream(self._to_langchain(messages)):
            yield chunk
