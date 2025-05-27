from typing import List, Optional
from dependency_injector.wiring import inject
from fastapi import HTTPException, UploadFile
from chunks.domain.model.image_schema import ChunkImageSchema
from chunks.domain.repository.chunk_repository import IChunkRepository
from chunks.domain.repository.image_repository import IImageRepository
from utils.object import get_object_id


class ImageService:

    @inject
    def __init__(
        self,
        image_repository: IImageRepository,
        chunk_repository: IChunkRepository,  # 순환 참조 회피를 위해 repository 주입
    ):
        self.image_repository = image_repository
        self.chunk_repository = chunk_repository

    async def create_image(self, image: ChunkImageSchema) -> ChunkImageSchema:
        return await self.image_repository.create_image(image)

    async def get_image(
        self,
        image_id: str,
        user_id: str,
    ) -> Optional[ChunkImageSchema]:
        oid = get_object_id(image_id)
        chunk_image = await self.image_repository.get_image(oid)

        if chunk_image is None:
            raise HTTPException(
                status_code=404,
                detail="Image를 찾을 수 없습니다.",
            )

        if chunk_image.creator != user_id:
            raise HTTPException(
                status_code=403,
                detail="Image를 조회할 권한이 없습니다.",
            )

        return chunk_image

    async def get_image_by_chunk_id(
        self, chunk_id: str, user_id: str
    ) -> List[ChunkImageSchema]:
        oid = get_object_id(chunk_id)
        chunk = await self.chunk_repository.get_chunk(oid)

        if chunk is None:
            raise HTTPException(
                status_code=404,
                detail="Chunk를 찾을 수 없습니다.",
            )

        if chunk.creator != user_id:
            raise HTTPException(
                status_code=403,
                detail="Chunk에 속한 Image를 조회할 권한이 없습니다.",
            )

        return await self.image_repository.get_image_by_chunk_id(chunk.id)

    async def update_image(
        self,
        image_id: str,
        description: str,
        user_id: str,
    ) -> ChunkImageSchema:

        oid = get_object_id(image_id)
        image = await self.image_repository.get_image(oid)

        if image.creator != user_id:
            raise HTTPException(
                status_code=403,
                detail="Image를 수정할 권한이 없습니다.",
            )

        image.image_description = description

        if await self.image_repository.update_image(oid, image):
            return image
        else:
            raise HTTPException(
                status_code=500,
                detail="Image 설명 수정 실패",
            )

    async def multimodal_description(
        self,
        image_id: str,
        user_id: str,
    ) -> ChunkImageSchema:
        pass

    async def delete_image(self, image_id: str):
        oid = get_object_id(image_id)
        return await self.image_repository.delete_image(oid)
