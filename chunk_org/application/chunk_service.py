from fastapi import HTTPException
from app.application.app_service import AppService
from app.domain.model.app_schema import AppSchema, MetaSchema
from chunk_org.domain.model.chunk_schema import ChunkSchema
from chunk_org.domain.repository.chunk_repository import IChunkRepository
from chunk_org.infra.chunk_repository_impl import ChunkRepository
from utils.file_utils import delete_image_folder
from utils.preprocess import chunking


class ChunkService:

    def __init__(self):
        self.chunk_repository: IChunkRepository = ChunkRepository()
        self.app_service = AppService()

    async def create_chunk_bulk(
        self,
        app_id: str,
        meta_id: str,
        chunk_size: int,
        chunk_overlap: int,
        user_id: str,
    ) -> list[ChunkSchema]:

        app: AppSchema = await self.app_service.get_app(app_id)
        meta: MetaSchema = await self.app_service.get_meta(app_id, meta_id)

        if app.creator != user_id and meta.creator != user_id:
            raise HTTPException(
                status_code=403,
                detail="청크 생성 권한이 없습니다.",
            )

        if meta.extension != "pdf":
            raise HTTPException(
                status_code=400,
                detail="현재 pdf 파일만 청크 생성 가능합니다.",
            )

        await self.delete_chunk_bulk(app_id, meta_id, user_id)

        file_path = meta.file_path
        img_save_path = f"{app_id}/{meta_id}"  # ABCD/1234

        # 페이지별 텍스트 처리 및 청킹
        documents = chunking(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            file_path=file_path,
            img_save_path=img_save_path,
        )

        chunk_list = []

        for doc in documents:
            chunk = ChunkSchema(
                page=doc.metadata.get("page", 0),
                tags=doc.metadata.get("tags", []),
                images=doc.metadata.get("images", []),
                content=doc.page_content,
                file_creation_date=doc.metadata.get("creationDate", ""),
                file_mod_date=doc.metadata.get("modDate", ""),
                creator=user_id,
            )
            chunk_list.append(chunk)

        await self.chunk_repository.create_chunk_bulk(
            app_id=app_id,
            meta_id=meta_id,
            chunk_list=chunk_list,
        )

        return chunk_list

    async def create_all_chunk(
        self,
        app_id: str,
        chunk_size: int,
        chunk_overlap: int,
        user_id: str,
    ) -> tuple[list[str], list[str]]:

        success_list = []
        error_list = []

        app: AppSchema = await self.app_service.get_app(app_id)

        if not app.metadata:
            raise HTTPException(
                status_code=400,
                detail="메타 정보가 없습니다.",
            )

        for meta in app.metadata:
            try:
                await self.create_chunk_bulk(
                    app_id=app_id,
                    meta_id=meta.id,
                    chunk_size=chunk_size,
                    chunk_overlap=chunk_overlap,
                    user_id=user_id,
                )
                success_list.append(meta.id)
            except Exception as e:
                error_list.append({"meta_id": meta.id, "message": str(e)})
                continue

        return success_list, error_list

    async def delete_chunk_bulk(
        self,
        app_id: str,
        meta_id: str,
        user_id: str,
    ) -> bool:

        app: AppSchema = await self.app_service.get_app(app_id)
        meta: MetaSchema = await self.app_service.get_meta(app_id, meta_id)

        if app.creator != user_id and meta.creator != user_id:
            raise HTTPException(
                status_code=403,
                detail="청크 삭제 권한이 없습니다.",
            )

        if meta.extension != "pdf":
            raise HTTPException(
                status_code=400,
                detail="pdf 파일이 아니기에 청크가 없습니다.",
            )

        img_save_path = f"{app_id}/{meta_id}"  # ABCD/1234
        delete_image_folder(img_save_path)

        return await self.chunk_repository.delete_chunk_bulk(app_id, meta_id)

    async def delete_all_chunk(
        self,
        app_id: str,
        user_id: str,
    ) -> bool:

        success_list = []
        error_list = []

        app: AppSchema = await self.app_service.get_app(app_id)

        for meta in app.metadata:
            try:
                await self.delete_chunk_bulk(app_id, meta.id, user_id)
                success_list.append(meta.id)
            except Exception as e:
                error_list.append({"meta_id": meta.id, "message": str(e)})
                continue

        return success_list, error_list

    def update_chunk(
        self,
        app_id: str,
        meta_id: str,
        chunk: ChunkSchema,
    ) -> bool:
        pass
