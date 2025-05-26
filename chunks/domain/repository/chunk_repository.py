from abc import ABC, abstractmethod
from typing import List, Optional

from bson import ObjectId

from chunks.domain.model.chunk_schema import ChunkSchema


class IChunkRepository(ABC):

    @abstractmethod
    async def create_chunk(self, chunk: ChunkSchema) -> ChunkSchema:
        """
        개별 청크를 DB에 저장한다.
        """
        pass

    @abstractmethod
    async def get_chunk(self, chunk_id: ObjectId) -> Optional[ChunkSchema]:
        """
        chunk_id에 해당하는 청크를 조회한다.
        """
        pass

    @abstractmethod
    async def get_chunk_by_document_id(
        self, document_id: ObjectId
    ) -> Optional[List[ChunkSchema]]:
        """
        document_id에 해당하는 청크를 조회한다.
        """
        pass

    @abstractmethod
    async def delete_chunk(self, chunk_id: ObjectId) -> bool:
        """
        chunk_id에 해당하는 청크를 삭제한다.
        """
        pass
