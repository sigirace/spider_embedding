from abc import ABC, abstractmethod
from typing import List, Optional

from bson import ObjectId

from chunks.domain.model.image_schema import ChunkImageSchema


class IImageRepository(ABC):

    @abstractmethod
    async def create_image(self, chunk: ChunkImageSchema) -> ChunkImageSchema:
        """
        개별 이미지를 DB에 저장한다.
        """
        pass

    @abstractmethod
    async def get_image(self, image_id: ObjectId) -> Optional[ChunkImageSchema]:
        """
        image_id에 해당하는 이미지를 조회한다.
        """
        pass

    @abstractmethod
    async def get_image_by_chunk_id(
        self, chunk_id: ObjectId
    ) -> Optional[List[ChunkImageSchema]]:
        """
        chunk_id에 해당하는 이미지를 조회한다.
        """
        pass

    @abstractmethod
    async def update_image(self, image_id: ObjectId, image: ChunkImageSchema) -> bool:
        """
        image_id에 해당하는 이미지를 수정한다.
        """
        pass

    @abstractmethod
    async def delete_image(self, image_id: ObjectId) -> bool:
        """
        image_id에 해당하는 이미지를 삭제한다.
        """
        pass
