from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from chunk_org.application.chunk_service import ChunkService
from chunk_org.interface.dto.chunk_dto import (
    ChunkAllRequest,
    ChunkAllResponse,
    ChunkRequest,
    ChunkResponse,
)
from common.log_config import get_logger
from containers import Container
from dependency_injector.wiring import Provide, inject

from user.domain.user import User
from user.interface.user_depends import get_current_user

logger = get_logger(__name__)

router = APIRouter(prefix="/chunk")


@router.post("/{app_id}/meta/{meta_id}")
@inject
async def create_chunk(
    chunk_req: ChunkRequest,
    chunk_service: ChunkService = Depends(Provide[Container.chunk_service]),
    user: User = Depends(get_current_user),
) -> list[ChunkResponse]:
    try:
        logger.info(
            f"[Chunk] 청크 생성 요청: {user.user_id} - {chunk_req.app_id}, {chunk_req.meta_id}"
        )
        chunk_list = await chunk_service.create_chunk_bulk(
            app_id=chunk_req.app_id,
            meta_id=chunk_req.meta_id,
            chunk_size=chunk_req.chunk_size,
            chunk_overlap=chunk_req.chunk_overlap,
            user_id=user.user_id,
        )

        chunk_response_list = [
            ChunkResponse(**chunk.model_dump()) for chunk in chunk_list
        ]

        logger.info(
            f"[Chunk] 청크 생성 완료: {user.user_id} - {chunk_req.app_id}, {chunk_req.meta_id}"
        )

        return chunk_response_list

    except ValueError as e:
        logger.error(
            f"[Chunk] 청크 생성 실패: {user.user_id} - {chunk_req.app_id}, {chunk_req.meta_id} => {e}"
        )
        raise HTTPException(status_code=400, detail=str(e))

    except Exception as e:
        logger.error(
            f"[Chunk] 청크 생성 실패: {user.user_id} - {chunk_req.app_id}, {chunk_req.meta_id} => {e}"
        )
        raise


@router.post("/{app_id}/all")
@inject
async def create_all_chunk(
    chunk_req: ChunkAllRequest,
    chunk_service: ChunkService = Depends(Provide[Container.chunk_service]),
    user: User = Depends(get_current_user),
) -> ChunkAllResponse:
    try:
        logger.info(f"[Chunk] 모든 청크 생성 요청: {user.user_id} - {chunk_req.app_id}")
        success_list, error_list = await chunk_service.create_all_chunk(
            app_id=chunk_req.app_id,
            chunk_size=chunk_req.chunk_size,
            chunk_overlap=chunk_req.chunk_overlap,
            user_id=user.user_id,
        )

        logger.info(f"[Chunk] 모든 청크 생성 완료: {user.user_id} - {chunk_req.app_id}")

        return ChunkAllResponse(
            success_list=success_list,
            error_list=error_list,
        )
    except ValueError as e:
        logger.error(
            f"[Chunk] 청크 생성 실패: {user.user_id} - {chunk_req.app_id} => {e}"
        )
        raise HTTPException(status_code=400, detail=str(e))

    except Exception as e:
        logger.error(
            f"[Chunk] 청크 생성 실패: {user.user_id} - {chunk_req.app_id} => {e}"
        )
        raise


@router.delete("/{app_id}/meta/{meta_id}")
@inject
async def delete_chunk(
    chunk_req: ChunkRequest,
    chunk_service: ChunkService = Depends(Provide[Container.chunk_service]),
    user: User = Depends(get_current_user),
) -> JSONResponse:
    try:
        logger.info(
            f"[Chunk] 청크 삭제 요청: {user.user_id} - {chunk_req.app_id}, {chunk_req.meta_id}"
        )
        await chunk_service.delete_chunk_bulk(
            app_id=chunk_req.app_id,
            meta_id=chunk_req.meta_id,
            user_id=user.user_id,
        )
        logger.info(
            f"[Chunk] 청크 삭제 완료: {user.user_id} - {chunk_req.app_id}, {chunk_req.meta_id}"
        )
        return JSONResponse(
            status_code=200,
            content={
                "message": f"{chunk_req.app_id} - {chunk_req.meta_id} 청크 삭제 완료"
            },
        )
    except ValueError as e:
        logger.error(
            f"[Chunk] 청크 삭제 실패: {user.user_id} - {chunk_req.app_id}, {chunk_req.meta_id} => {e}"
        )
        raise HTTPException(status_code=400, detail=str(e))

    except Exception as e:
        logger.error(
            f"[Chunk] 청크 삭제 실패: {user.user_id} - {chunk_req.app_id}, {chunk_req.meta_id} => {e}"
        )
        raise


@router.delete("/{app_id}/all")
@inject
async def delete_all_chunk(
    chunk_req: ChunkAllRequest,
    chunk_service: ChunkService = Depends(Provide[Container.chunk_service]),
    user: User = Depends(get_current_user),
) -> ChunkAllResponse:
    try:
        logger.info(f"[Chunk] 모든 청크 삭제 요청: {user.user_id} - {chunk_req.app_id}")
        success_list, error_list = await chunk_service.delete_all_chunk(
            app_id=chunk_req.app_id,
            user_id=user.user_id,
        )
        logger.info(f"[Chunk] 모든 청크 삭제 완료: {user.user_id} - {chunk_req.app_id}")
        return ChunkAllResponse(
            success_list=success_list,
            error_list=error_list,
        )
    except ValueError as e:
        logger.error(
            f"[Chunk] 청크 삭제 실패: {user.user_id} - {chunk_req.app_id} => {e}"
        )
        raise HTTPException(status_code=400, detail=str(e))

    except Exception as e:
        logger.error(
            f"[Chunk] 청크 삭제 실패: {user.user_id} - {chunk_req.app_id} => {e}"
        )
        raise
