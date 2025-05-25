from abc import ABC, abstractmethod

from chunk_org.domain.model.chunk_schema import ChunkSchema


class IChunkRepository(ABC):
    @abstractmethod
    def create_chunk_bulk(
        self, app_id: str, meta_id: str, chunk_list: list[ChunkSchema]
    ) -> None:
        pass

    @abstractmethod
    def delete_chunk_bulk(self, app_id: str, meta_id: str) -> bool:
        pass

    @abstractmethod
    def update_chunk(self, app_id: str, meta_id: str, chunk: ChunkSchema) -> bool:
        pass
