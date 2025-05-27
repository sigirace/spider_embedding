from typing import List
from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from dependency_injector.wiring import inject, Provide
from chunks.application.chunk_service import ChunkService
from common.log_config import get_logger
from containers import Container
from document.application.document_service import DocumentService
from document.interface.dto.document_dto import (
    DocumentDeleteListRequest,
    DocumentUpdateRequest,
)
from document.interface.dto.document_mapper import DocumentMapper
from user.domain.user import User
from user.interface.user_depends import get_current_user

logger = get_logger(__name__)

router = APIRouter(prefix="/document")


@router.post("/{app_id}")
@inject
async def create_document(
    app_id: str,
    file_list: List[UploadFile] = File(default=None),
    document_service: DocumentService = Depends(Provide[Container.document_service]),
    user: User = Depends(get_current_user),
):
    try:
        """
        app_id
        """
        logger.info(f"[Document] {user.user_id}: {app_id} 문서 생성 요청")

        success_list, error_list = await document_service.create_document(
            app_id=app_id,
            file_list=file_list,
            user_id=user.user_id,
        )

        return DocumentMapper.to_document_list_response(success_list, error_list)

    except HTTPException as e:
        logger.error(f"[Document] {user.user_id}: 문서 생성 실패, detail: {e.detail}")
        raise
    except Exception as e:
        logger.exception(
            f"[Document] {user.user_id}: 문서 생성 중 알 수 없는 오류 - {str(e)}"
        )
        raise HTTPException(
            status_code=500,
            detail="문서 생성 중 서버 오류가 발생했습니다.",
        )


@router.get("/{document_id}")
@inject
async def get_document(
    document_id: str,
    document_service: DocumentService = Depends(Provide[Container.document_service]),
    user: User = Depends(get_current_user),
):
    try:
        logger.info(f"[Document] {user.user_id}: {document_id} 문서 조회")
        document = await document_service.get_document(document_id)
        logger.info(f"[Document] {user.user_id}: {document_id} 문서 조회 완료")
        return DocumentMapper.to_document_response(document)
    except HTTPException as e:
        logger.error(f"[Document] {user.user_id}: 문서 조회 실패, detail: {str(e)}")
        raise
    except Exception as e:
        logger.exception(
            f"[Document] {user.user_id}: 문서 조회 중 알 수 없는 오류 - {str(e)}"
        )
        raise HTTPException(
            status_code=500,
            detail="문서 조회 중 서버 오류가 발생했습니다.",
        )


@router.get("/{app_id}/list")
@inject
async def get_document_by_app(
    app_id: str,
    document_service: DocumentService = Depends(Provide[Container.document_service]),
    user: User = Depends(get_current_user),
):
    try:
        logger.info(f"[Document] {user.user_id}: {app_id} 문서 목록 조회")
        document_list = await document_service.get_document_by_app(app_id)
        logger.info(f"[Document] {user.user_id}: {app_id} 문서 목록 조회 완료")
        return [
            DocumentMapper.to_document_response(document) for document in document_list
        ]
    except HTTPException as e:
        logger.error(
            f"[Document] {user.user_id}: 문서 목록 조회 실패, detail: {e.detail}"
        )
        raise
    except Exception as e:
        logger.exception(
            f"[Document] {user.user_id}: 문서 목록 조회 중 알 수 없는 오류 - {str(e)}"
        )
        raise HTTPException(
            status_code=500,
            detail="문서 목록 조회 중 서버 오류가 발생했습니다.",
        )


@router.put("/{document_id}")
@inject
async def update_document(
    document_id: str,
    req: DocumentUpdateRequest,
    document_service: DocumentService = Depends(Provide[Container.document_service]),
    user: User = Depends(get_current_user),
):
    try:
        logger.info(f"[Document] {user.user_id}: {document_id} 문서 수정")
        document = await document_service.update_document(
            document_id=document_id,
            req=DocumentMapper.to_document_update_schema(req=req),
            user_id=user.user_id,
        )
        logger.info(f"[Document] {user.user_id}: {document_id} 문서 수정 완료")
        return DocumentMapper.to_document_response(document)
    except HTTPException as e:
        logger.error(f"[Document] {user.user_id}: 문서 수정 실패, detail: {e.detail}")
        raise
    except Exception as e:
        logger.exception(
            f"[Document] {user.user_id}: 문서 수정 중 알 수 없는 오류 - {str(e)}"
        )
        raise HTTPException(
            status_code=500,
            detail="문서 수정 중 서버 오류가 발생했습니다.",
        )


@router.delete("/{app_id}/list")
@inject
async def delete_document_list(
    app_id: str,
    req: DocumentDeleteListRequest,
    document_service: DocumentService = Depends(Provide[Container.document_service]),
    chunk_service: ChunkService = Depends(Provide[Container.chunk_service]),
    user: User = Depends(get_current_user),
):
    try:
        logger.info(f"[Document] {user.user_id}: 문서 목록 삭제")

        for document_id in req.document_list:
            await chunk_service.delete_chunk_by_document_id(
                document_id=document_id,
                user_id=user.user_id,
            )

        success_list, error_list = await document_service.delete_document_list(
            app_id=app_id,
            document_list=req.document_list,
            user_id=user.user_id,
        )

        logger.info(f"[Document] {user.user_id}: 문서 목록 삭제 완료")
        return DocumentMapper.to_document_delete_list_response(
            success_list=success_list,
            error_list=error_list,
        )
    except HTTPException as e:
        logger.error(
            f"[Document] {user.user_id}: 문서 목록 삭제 실패, detail: {e.detail}"
        )
        raise
    except Exception as e:
        logger.exception(
            f"[Document] {user.user_id}: 문서 목록 삭제 중 알 수 없는 오류 - {str(e)}"
        )
        raise HTTPException(
            status_code=500,
            detail="문서 목록 삭제 중 서버 오류가 발생했습니다.",
        )


@router.delete("/{document_id}")
@inject
async def delete_document(
    document_id: str,
    document_service: DocumentService = Depends(Provide[Container.document_service]),
    chunk_service: ChunkService = Depends(Provide[Container.chunk_service]),
    user: User = Depends(get_current_user),
):
    try:
        logger.info(f"[Document] {user.user_id}: {document_id} 문서 삭제")

        await chunk_service.delete_chunk_by_document_id(
            document_id=document_id,
            user_id=user.user_id,
        )

        delete_result = await document_service.delete_document(
            document_id=document_id,
            user_id=user.user_id,
        )
        logger.info(f"[Document] {user.user_id}: {document_id} 문서 삭제 완료")
        return DocumentMapper.to_document_delete_response(delete_result)
    except HTTPException as e:
        logger.error(f"[Document] {user.user_id}: 문서 삭제 실패, detail: {e.detail}")
        raise
    except Exception as e:
        logger.exception(
            f"[Document] {user.user_id}: 문서 삭제 중 알 수 없는 오류 - {str(e)}"
        )
        raise HTTPException(
            status_code=500,
            detail="문서 삭제 중 서버 오류가 발생했습니다.",
        )
