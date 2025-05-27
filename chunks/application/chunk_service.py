from typing import List, Optional
from dependency_injector.wiring import inject
from fastapi import HTTPException

from app.application.app_service import AppService
from chunks.application.image_service import ImageService
from chunks.domain.model.chunk_schema import (
    ChunkBulkCreateSchema,
    ChunkCreateErrorSchema,
    ChunkCreateSuccessSchema,
    ChunkParameterSchema,
    ChunkSchema,
)
from chunks.domain.model.image_schema import ChunkImageSchema
from chunks.domain.repository.chunk_repository import IChunkRepository
from document.application.document_service import DocumentService
from document.domain.model.document_schema import DocumentSchema
from utils.object import get_object_id, get_str_id
from utils.preprocess import chunking


class ChunkService:

    @inject
    def __init__(
        self,
        app_service: AppService,
        document_service: DocumentService,
        image_service: ImageService,
        chunk_repository: IChunkRepository,
    ):
        self.app_service = app_service
        self.chunk_repository = chunk_repository
        self.document_service = document_service
        self.image_service = image_service

    async def create_chunk_by_document(
        self,
        document_id: str,
        chunk_parameter: ChunkParameterSchema,
        user_id: str,
        pre_auth_check: bool = False,
        document_schema: DocumentSchema | None = None,
    ) -> List[ChunkSchema]:

        document = document_schema or await self.document_service.get_document(
            document_id
        )

        if document.extension != "pdf":
            raise HTTPException(
                status_code=400,
                detail="현재 pdf 파일만 청크 생성 가능합니다.",
            )

        if not pre_auth_check:
            if document.creator != user_id:
                raise HTTPException(
                    status_code=403,
                    detail="Document에 chunk를 생성할 권한이 없습니다.",
                )

        await self.delete_chunk_by_document_id(
            document_id=document_id,
            user_id=user_id,
            pre_auth_check=True,
            document_schema=document,
        )

        try:
            file_path = (
                document.file_path
            )  # ./static/data/app_id/source/document.name.extension
            img_save_path = f"{document.app_id}/{document.id}"  # app_id/document_id

            _documents = chunking(
                chunk_size=chunk_parameter.chunk_size,
                chunk_overlap=chunk_parameter.chunk_overlap,
                file_path=file_path,
                img_save_path=img_save_path,
            )

        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Document Preprocessing 중 오류 발생: {e}",
            )

        chunk_list: List[ChunkSchema] = []
        image_list: List[ChunkImageSchema] = []

        for doc in _documents:
            try:

                chunk_schema = ChunkSchema(
                    content=doc.page_content,
                    tags=doc.metadata.get("tags", []),
                    page=doc.metadata.get("page", 0),
                    file_creation_date=doc.metadata.get("creationDate", ""),
                    file_mod_date=doc.metadata.get("modDate", ""),
                    document_id=document.id,
                    creator=user_id,
                )

                _images = doc.metadata.get("images", [])

                for image in _images:
                    chunk_image_schema = await self.image_service.create_image(
                        ChunkImageSchema(
                            chunk_id=chunk_schema.id,
                            image_url=image,
                            creator=user_id,
                        )
                    )
                    image_list.append(chunk_image_schema)

                await self.chunk_repository.create_chunk(chunk_schema)
                chunk_list.append(chunk_schema)

            except Exception as e:

                # rollback

                for image in image_list:
                    await self.image_service.delete_image(image.id)

                for chunk in chunk_list:
                    await self.chunk_repository.delete_chunk(chunk.id)

                raise HTTPException(
                    status_code=500,
                    detail=f"Chunk 생성 중 오류 발생: {e}",
                )

        return chunk_list

    async def create_chunk_by_app(
        self,
        app_id: str,
        chunk_parameter: ChunkParameterSchema,
        user_id: str,
    ) -> ChunkBulkCreateSchema:

        app = await self.app_service.get_app(app_id)

        if app.creator != user_id:
            raise HTTPException(
                status_code=403,
                detail="App에 chunk를 생성할 권한이 없습니다.",
            )

        document_list = await self.document_service.get_document_by_app(
            app_id=app_id,
        )

        success_document_list: List[ChunkCreateSuccessSchema] = []
        error_document_list: List[ChunkCreateErrorSchema] = []

        for document in document_list:

            try:

                chunk_list = await self.create_chunk_by_document(
                    document_id=get_str_id(document.id),
                    chunk_parameter=chunk_parameter,
                    user_id=user_id,
                    pre_auth_check=True,
                    document_schema=document,
                )

                success_document_list.append(
                    ChunkCreateSuccessSchema(
                        document_id=document.id,
                        chunk_list=chunk_list,
                    )
                )
            except Exception as e:
                error_document_list.append(
                    ChunkCreateErrorSchema(
                        document_id=document.id,
                        error=str(e),
                    )
                )

        return ChunkBulkCreateSchema(
            success_document_list=success_document_list,
            error_document_list=error_document_list,
        )

    async def get_chunk(
        self,
        chunk_id: str,
        user_id: str,
    ) -> ChunkSchema:

        chunk: Optional[ChunkSchema] = await self.chunk_repository.get_chunk(
            get_object_id(chunk_id),
        )

        if chunk is None:
            raise HTTPException(
                status_code=404,
                detail="Chunk를 찾을 수 없습니다.",
            )

        if chunk.creator != user_id:
            raise HTTPException(
                status_code=403,
                detail="Chunk를 조회할 권한이 없습니다.",
            )

        return chunk

    async def get_chunk_by_document_id(
        self,
        document_id: str,
        user_id: str,
        pre_auth_check: bool = False,
        document_schema: DocumentSchema | None = None,
    ) -> List[ChunkSchema]:

        document = document_schema or await self.document_service.get_document(
            document_id
        )

        if not pre_auth_check:
            if document.creator != user_id:
                raise HTTPException(
                    status_code=403,
                    detail="Document의 chunk를 조회할 권한이 없습니다.",
                )

        try:
            return await self.chunk_repository.get_chunk_by_document_id(document.id)
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Document의 Chunk 조회 중 오류 발생: {e}",
            )

    async def delete_chunk(
        self,
        chunk_id: str,
        user_id: str,
    ) -> bool:

        chunk = await self.get_chunk(
            chunk_id=chunk_id,
            user_id=user_id,
        )

        img_list = await self.image_service.get_image_by_chunk_id(
            get_str_id(chunk.id), user_id
        )

        rollback_list: List[ChunkImageSchema] = []

        try:
            for image in img_list:
                if await self.image_service.delete_image(get_str_id(image.id)):
                    rollback_list.append(image)

            return await self.chunk_repository.delete_chunk(chunk.id)
        except Exception as e:
            for image in rollback_list:
                await self.image_service.create_image(image)

            raise HTTPException(
                status_code=500,
                detail=f"Chunk 삭제 중 오류 발생: {str(e)}",
            )

    async def delete_chunk_by_document_id(
        self,
        document_id: str,
        user_id: str,
        pre_auth_check: bool = False,
        document_schema: DocumentSchema | None = None,
    ) -> bool:

        document = document_schema or await self.document_service.get_document(
            document_id
        )

        if not pre_auth_check:

            if document.creator != user_id:
                raise HTTPException(
                    status_code=403,
                    detail="Document의 chunk를 삭제할 권한이 없습니다.",
                )

        chunk_list: List[ChunkSchema] = await self.get_chunk_by_document_id(
            document_id=document_id,
            user_id=user_id,
            pre_auth_check=True,
            document_schema=document,
        )

        doc_rollback_list: List[ChunkSchema] = []
        img_rollback_list: List[ChunkImageSchema] = []

        for chunk in chunk_list:
            try:

                img_list = await self.image_service.get_image_by_chunk_id(
                    get_str_id(chunk.id),
                    user_id,
                )

                for image in img_list:
                    if await self.image_service.delete_image(image.id):
                        img_rollback_list.append(image)

                if await self.chunk_repository.delete_chunk(chunk.id):
                    doc_rollback_list.append(chunk)

            except Exception as e:

                for image in img_rollback_list:
                    await self.image_service.create_image(image)

                for chunk in doc_rollback_list:
                    await self.chunk_repository.create_chunk(chunk)

                raise HTTPException(
                    status_code=500,
                    detail=f"Chunk 삭제 중 오류 발생: {e}",
                )

        return True

    async def delete_chunk_by_app_id(
        self,
        app_id: str,
        user_id: str,
    ) -> bool:

        app = await self.app_service.get_app(app_id)

        if app.creator != user_id:
            raise HTTPException(
                status_code=403,
                detail="App에 chunk를 삭제할 권한이 없습니다.",
            )

        document_list = await self.document_service.get_document_by_app(
            app_id=app_id,
        )

        rollback_list: List[DocumentSchema] = []
        try:
            for document in document_list:

                await self.delete_chunk_by_document_id(
                    document_id=get_str_id(document.id),
                    user_id=user_id,
                    pre_auth_check=True,  # app에 대한 권한이 있으면 document에 대한 권한도 있음
                    document_schema=document,
                )
                rollback_list.append(document)

        except Exception as e:
            for document in rollback_list:
                await self.document_service.create_document(document)

            raise HTTPException(
                status_code=500,
                detail=f"Chunk 삭제 중 오류 발생: {e}",
            )

        return True
