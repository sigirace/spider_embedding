from typing import List
from fastapi import APIRouter, Depends, HTTPException

from chunks.application.chunk_service import ChunkService
from chunks.domain.model.chunk_schema import ChunkSchema
from dependency_injector.wiring import inject, Provide

from chunks.interface.dto.chunk_dto import ChunkParameterRequest
from chunks.interface.dto.chunk_mapper import ChunkMapper
from common.dto import CommonResponse
from containers import Container
from user.domain.user import User
from user.interface.user_depends import get_current_user
from common.log_config import get_logger

router = APIRouter(prefix="/chunk")


logger = get_logger(__name__)


@router.post("/app/{app_id}")
@inject
async def create_chunk_by_app(
    app_id: str,
    chunk_parameter: ChunkParameterRequest,
    chunk_service: ChunkService = Depends(Provide[Container.chunk_service]),
    user: User = Depends(get_current_user),
):
    try:
        logger.info(f"Chunk 생성 요청: {user.user_id}-{app_id}")
        chunk_bulk_create_schema = await chunk_service.create_chunk_by_app(
            app_id=app_id,
            chunk_parameter=ChunkMapper.to_chunk_parameter_schema(chunk_parameter),
            user_id=user.user_id,
        )
        logger.info(f"Chunk 생성 완료: {user.user_id} -> app_id: {app_id}")

        return ChunkMapper.to_chunk_bulk_create_response(chunk_bulk_create_schema)

    except HTTPException as e:
        logger.error(
            f"Chunk 생성 중 오류 발생: {user.user_id} -> app_id: {app_id}, error: {e.detail}"
        )
        raise
    except Exception as e:
        logger.error(
            f"Chunk 생성 중 오류 발생: {user.user_id} -> app_id: {app_id}, error: {str(e)}"
        )
        raise HTTPException(
            status_code=500,
            detail=f"Chunk 생성 중 오류 발생: {user.user_id} -> app_id: {app_id}, error: {str(e)}",
        )


@router.post("/document/{document_id}")
@inject
async def create_chunk_by_document(
    document_id: str,
    chunk_parameter: ChunkParameterRequest,
    chunk_service: ChunkService = Depends(Provide[Container.chunk_service]),
    user: User = Depends(get_current_user),
):
    try:
        logger.info(f"Chunk 생성 요청: {user.user_id}-> document_id: {document_id}")
        chunk_list = await chunk_service.create_chunk_by_document(
            document_id=document_id,
            chunk_parameter=ChunkMapper.to_chunk_parameter_schema(chunk_parameter),
            user_id=user.user_id,
        )
        logger.info(f"Chunk 생성 완료: {user.user_id} -> document_id: {document_id}")

        return [ChunkMapper.to_chunk_response(chunk) for chunk in chunk_list]

    except HTTPException as e:
        logger.error(
            f"Chunk 생성 중 오류 발생: {user.user_id} -> document_id: {document_id}, error: {e.detail}"
        )
        raise
    except Exception as e:
        logger.error(
            f"Chunk 생성 중 오류 발생: {user.user_id} -> document_id: {document_id}, error: {str(e)}"
        )
        raise HTTPException(
            status_code=500,
            detail=f"Chunk 생성 중 오류 발생: {str(e)}",
        )


@router.get("/{chunk_id}")
@inject
async def get_chunk(
    chunk_id: str,
    chunk_service: ChunkService = Depends(Provide[Container.chunk_service]),
    user: User = Depends(get_current_user),
):
    try:
        logger.info(f"Chunk 조회 요청: {user.user_id} -> chunk_id: {chunk_id}")
        chunk = await chunk_service.get_chunk(
            chunk_id=chunk_id,
            user_id=user.user_id,
        )
        logger.info(f"Chunk 조회 완료: {user.user_id} -> chunk_id: {chunk_id}")
        return ChunkMapper.to_chunk_response(chunk)
    except HTTPException as e:
        logger.error(
            f"Chunk 조회 중 오류 발생: {user.user_id} -> chunk_id: {chunk_id}, error: {e.detail}"
        )
        raise
    except Exception as e:
        logger.error(
            f"Chunk 조회 중 오류 발생: {user.user_id} -> chunk_id: {chunk_id}, error: {str(e)}"
        )
        raise HTTPException(
            status_code=500,
            detail=f"Chunk 조회 중 오류 발생: {str(e)}",
        )


@router.get("/document/{document_id}")
@inject
async def get_chunk_by_document(
    document_id: str,
    chunk_service: ChunkService = Depends(Provide[Container.chunk_service]),
    user: User = Depends(get_current_user),
):
    try:
        logger.info(
            f"Document의 Chunk 조회 요청: {user.user_id} -> document_id: {document_id}"
        )
        chunk_list = await chunk_service.get_chunk_by_document_id(
            document_id=document_id,
            user_id=user.user_id,
        )
        logger.info(
            f"Document의 Chunk 조회 완료: {user.user_id} -> document_id: {document_id}"
        )
        return [ChunkMapper.to_chunk_response(chunk) for chunk in chunk_list]
    except HTTPException as e:
        logger.error(
            f"Document의 Chunk 조회 중 오류 발생: {user.user_id} -> document_id: {document_id}, error: {e.detail}"
        )
        raise
    except Exception as e:
        logger.error(
            f"Document의 Chunk 조회 중 오류 발생: {user.user_id} -> document_id: {document_id}, error: {str(e)}"
        )
        raise HTTPException(
            status_code=500,
            detail=f"Document의 Chunk 조회 중 오류 발생: {str(e)}",
        )


@router.delete("/{chunk_id}")
@inject
async def delete_chunk(
    chunk_id: str,
    chunk_service: ChunkService = Depends(Provide[Container.chunk_service]),
    user: User = Depends(get_current_user),
):
    try:
        logger.info(f"Chunk 삭제 요청: {user.user_id} -> chunk_id: {chunk_id}")
        await chunk_service.delete_chunk(chunk_id=chunk_id, user_id=user.user_id)
        logger.info(f"Chunk 삭제 완료: {user.user_id} -> chunk_id: {chunk_id}")
        return CommonResponse(message=f"{chunk_id} Chunk 삭제 완료")
    except HTTPException as e:
        logger.error(
            f"Chunk 삭제 중 오류 발생: {user.user_id} -> chunk_id: {chunk_id}, error: {e.detail}"
        )
        raise
    except Exception as e:
        logger.error(
            f"Chunk 삭제 중 오류 발생: {user.user_id} -> chunk_id: {chunk_id}, error: {str(e)}"
        )
        raise HTTPException(
            status_code=500,
            detail=f"Chunk 삭제 중 오류 발생: {str(e)}",
        )


@router.delete("/document/{document_id}")
@inject
async def delete_chunk_by_document(
    document_id: str,
    chunk_service: ChunkService = Depends(Provide[Container.chunk_service]),
    user: User = Depends(get_current_user),
):
    try:
        logger.info(
            f"Document의 Chunk 삭제 요청: {user.user_id} -> document_id: {document_id}"
        )
        await chunk_service.delete_chunk_by_document_id(
            document_id=document_id,
            user_id=user.user_id,
        )
        logger.info(
            f"Document의 Chunk 삭제 완료: {user.user_id} -> document_id: {document_id}"
        )
        return CommonResponse(message=f"{document_id} Document의 Chunk 삭제 완료")
    except HTTPException as e:
        logger.error(
            f"Document의 Chunk 삭제 중 오류 발생: {user.user_id} -> document_id: {document_id}, error: {e.detail}"
        )
        raise
    except Exception as e:
        logger.error(
            f"Document의 Chunk 삭제 중 오류 발생: {user.user_id} -> document_id: {document_id}, error: {str(e)}"
        )
        raise HTTPException(
            status_code=500,
            detail=f"Document의 Chunk 삭제 중 오류 발생: {str(e)}",
        )
