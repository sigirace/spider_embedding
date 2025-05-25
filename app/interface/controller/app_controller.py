from fastapi import APIRouter, Depends, HTTPException

from app.interface.dto.app_mapper import AppMapper
from common.dto import CommonResponse
from containers import Container
from dependency_injector.wiring import Provide, inject

from app.application.app_service import AppService
from app.interface.dto.app_dto import (
    AppCreateRequest,
    AppDetailRequest,
)
from document.application.document_service import DocumentService
from user.domain.user import User
from user.interface.user_depends import get_current_user
from common.log_config import get_logger

logger = get_logger(__name__)

router = APIRouter(prefix="/app")


@router.post("")
@inject
async def create_app(
    req: AppCreateRequest,
    app_service: AppService = Depends(Provide[Container.app_service]),
    user: User = Depends(get_current_user),
):
    try:
        logger.info(f"[App] {user.user_id}: {req.app_name} 정보 생성")
        create_app_schema = AppMapper.to_app_create_schema(req, user.user_id)
        app = await app_service.create_app(
            app_schema=create_app_schema,
        )

        response = AppMapper.to_app_response(app)

        logger.info(f"[App] {user.user_id}: {app.app_name} 정보 생성 완료")

        return response
    except ValueError as e:
        # 4글자에 대한 에러메세지
        logger.error(
            f"[App] {user.user_id}: {req.app_name} 정보 생성 실패, detail: {str(e)}"
        )
        raise HTTPException(status_code=400, detail=str(e))
    except HTTPException as e:
        logger.error(
            f"[App] {user.user_id}: {req.app_name} 정보 생성 실패, detail: {str(e)}"
        )
        raise
    except Exception as e:
        logger.exception(
            f"[App] {user.user_id}: {req.app_name} 정보 생성 중 알 수 없는 오류 - {str(e)}"
        )
        raise HTTPException(
            status_code=500,
            detail="App 생성 중 서버 오류가 발생했습니다.",
        )


@router.get("/list")
@inject
async def get_app_list(
    app_service: AppService = Depends(Provide[Container.app_service]),
    user: User = Depends(get_current_user),
):
    try:
        logger.info(f"[App] {user.user_id}: 정보 목록 조회")
        app_list = await app_service.get_app_list(user.user_id)
        logger.info(f"[App] {user.user_id}: 정보 목록 조회 완료")

        return [AppMapper.to_app_response(app) for app in app_list]
    except HTTPException as e:
        logger.error(f"[App] {user.user_id}: 정보 목록 조회 실패, detail: {str(e)}")
        raise
    except Exception as e:
        logger.exception(
            f"[App] {user.user_id}: 정보 목록 조회 중 알 수 없는 오류 - {str(e)}"
        )
        raise HTTPException(
            status_code=500,
            detail="앱 삭제 중 서버 오류가 발생했습니다.",
        )


@router.get("/{app_id}")
@inject
async def get_app(
    app_id: str,
    app_service: AppService = Depends(Provide[Container.app_service]),
    user: User = Depends(get_current_user),
):
    try:
        logger.info(f"[App] {user.user_id}: {app_id} 정보 요청")
        app = await app_service.get_app(app_id)
        logger.info(f"[App] {user.user_id}: {app_id} 정보 요청 완료")

        return AppMapper.to_app_response(app)
    except HTTPException as e:
        logger.error(f"[App] {user.user_id}: {app_id} 정보 조회 실패, detail: {str(e)}")
        raise
    except Exception as e:
        logger.exception(f"[App] {user.user_id}: {app_id} 알 수 없는 오류 - {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="App 목록 조회 중 서버 오류가 발생했습니다.",
        )


@router.put("/{app_id}")
@inject
async def update_app(
    app_id: str,
    req: AppDetailRequest,
    app_service: AppService = Depends(Provide[Container.app_service]),
    user: User = Depends(get_current_user),
):
    try:
        logger.info(f"[App] {user.user_id}: {app_id} 정보 수정")
        updated_detail_schema = AppMapper.to_app_detail_schema(req)
        app = await app_service.update_app(
            id=app_id,
            req=updated_detail_schema,
            user_id=user.user_id,
        )
        logger.info(f"[App] {user.user_id}: {app_id} 정보 수정 완료")

        return AppMapper.to_app_response(app)
    except HTTPException as e:
        logger.error(f"[App] {user.user_id}: {app_id} 정보 수정 실패, detail: {str(e)}")
        raise
    except Exception as e:
        logger.exception(
            f"[App] {user.user_id}: {app_id} 정보 수정 중 알 수 없는 오류 - {str(e)}"
        )
        raise HTTPException(
            status_code=500,
            detail="App 수정 중 서버 오류가 발생했습니다.",
        )


@router.delete("/{app_id}")
@inject
async def delete_app(
    app_id: str,
    app_service: AppService = Depends(Provide[Container.app_service]),
    document_service: DocumentService = Depends(Provide[Container.document_service]),
    user: User = Depends(get_current_user),
):
    try:

        logger.info(f"[App] {user.user_id}: {app_id} 정보 삭제 요청")

        logger.info(f"[App] {user.user_id}: {app_id} 문서 목록 삭제 수행")

        _, error_list = await document_service.delete_document_list(
            app_id=app_id,
            document_list=None,
            user_id=user.user_id,
        )

        if error_list:
            logger.error(
                f"[App] {user.user_id}: {app_id} 삭제 실패 - 문서 삭제 중 오류 발생. 실패 항목: {[e.name for e in error_list]}"
            )
            raise HTTPException(
                status_code=400,
                detail=[e.model_dump() for e in error_list],
            )

        logger.info(f"[App] {user.user_id}: {app_id} 문서 목록 삭제 수행 완료")

        await app_service.delete_app(
            id=app_id,
            user_id=user.user_id,
        )

        logger.info(f"[App] {user.user_id}: {app_id} 삭제 완료")

        return CommonResponse(
            message=f"{app_id} 삭제 완료",
        )
    except HTTPException as e:
        logger.error(f"[App] {user.user_id}: {app_id} 삭제 실패, detail: {str(e)}")
        raise
    except Exception as e:
        logger.exception(
            f"[App] {user.user_id}: {app_id} 삭제 중 알 수 없는 오류 - {str(e)}"
        )
        raise HTTPException(
            status_code=500,
            detail="App 삭제 중 서버 오류가 발생했습니다.",
        )
