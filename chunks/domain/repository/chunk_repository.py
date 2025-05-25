from abc import ABC, abstractmethod

from chunks.domain.model.chunk_schema import ChunkSchema


class IChunkRepository(ABC):

    @abstractmethod
    def create_chunk(self, chunk: ChunkSchema) -> ChunkSchema:
        """
        개별 청크를 DB에 저장한다.
        """
        pass
