from abc import ABC, abstractmethod
from typing import AsyncGenerator, Generator, List
from llm.domain.model.llm_schema import Message


class ILLMRepository(ABC):
    """Port that defines every interaction we need with an LLM."""

    # blocking call
    @abstractmethod
    def invoke(self, messages: List[Message]) -> str:
        pass

    # async call
    @abstractmethod
    async def ainvoke(self, messages: List[Message]) -> str:
        pass

    # streaming (sync generator)
    @abstractmethod
    def stream(self, messages: List[Message]) -> Generator[str, None, None]:
        pass

    # async streaming
    @abstractmethod
    async def astream(self, messages: List[Message]) -> AsyncGenerator[str, None]:
        pass
