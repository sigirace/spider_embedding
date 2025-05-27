import base64
import mimetypes
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import FileResponse, JSONResponse
from chunks.application.image_service import ImageService
from chunks.interface.dto.image_dto import ChunkImageUpdateRequest
from chunks.interface.dto.image_mapper import ChunkImageMapper
from common.dto import CommonResponse
from common.log_config import get_logger
from containers import Container
from dependency_injector.wiring import Provide, inject
from user.domain.user import User
from user.interface.user_depends import get_current_user

router = APIRouter(prefix="/image")

logger = get_logger(__name__)


@router.get("/chunk/{chunk_id}")
@inject
async def get_image_by_chunk_id(
    chunk_id: str,
    image_service: ImageService = Depends(Provide[Container.image_service]),
    user: User = Depends(get_current_user),
):
    try:
        logger.info(
            f"[Image] Chunk에 속한 Image 조회 요청: {user.user_id} -> {chunk_id}"
        )
        chunk_image_list = await image_service.get_image_by_chunk_id(
            chunk_id,
            user.user_id,
        )

        logger.info(
            f"[Image] Chunk에 속한 Image 조회 완료: {user.user_id} -> {chunk_id}"
        )

        return [
            ChunkImageMapper.to_chunk_image_response(image)
            for image in chunk_image_list
        ]
    except HTTPException as e:
        logger.error(
            f"[Image] Image 조회 중 오류 발생 : {user.user_id} -> {chunk_id}, detail: {e}"
        )
        raise
    except Exception as e:
        logger.error(f"Image 조회 중 오류 발생: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Image 조회 중 오류 발생: {e}",
        )


@router.get("/{image_id}")
@inject
async def get_image(
    image_id: str,
    image_service: ImageService = Depends(Provide[Container.image_service]),
    user: User = Depends(get_current_user),
):
    try:
        logger.info(f"Image 조회 요청: {user.user_id} -> {image_id}")
        image = await image_service.get_image(
            image_id,
            user.user_id,
        )
        logger.info(f"Image 조회 완료: {user.user_id} -> {image_id}")
        return ChunkImageMapper.to_chunk_image_response(image)
    except HTTPException as e:
        logger.error(
            f"[Image] Image 조회 중 오류 발생 : {user.user_id} -> {image_id}, detail: {e}"
        )
        raise
    except Exception as e:
        logger.error(
            f"[Image] Image 조회 중 오류 발생 : {user.user_id} -> {image_id}, detail: {e}"
        )
        raise HTTPException(
            status_code=500,
            detail=f"Image 조회 중 오류 발생: {e}",
        )


@router.get("/show/{image_id}")
@inject
async def show_image_directly(
    image_id: str,
    image_service: ImageService = Depends(Provide[Container.image_service]),
    user: User = Depends(get_current_user),
):
    image = await image_service.get_image(
        image_id,
        user.user_id,
    )

    file_path = image.image_url
    mime_type, _ = mimetypes.guess_type(file_path)
    return FileResponse(file_path, media_type=mime_type)


@router.get("/show/base64/{image_id}")
@inject
async def get_image_data_url(
    image_id: str,
    image_service: ImageService = Depends(Provide[Container.image_service]),
    user: User = Depends(get_current_user),
):

    image = await image_service.get_image(
        image_id,
        user.user_id,
    )

    file_path = image.image_url
    mime_type, _ = mimetypes.guess_type(file_path)
    with open(file_path, "rb") as f:
        encoded = base64.b64encode(f.read()).decode("utf-8")
    data_url = f"data:{mime_type};base64,{encoded}"
    return JSONResponse(content={"data_url": data_url})


@router.put("/{image_id}")
@inject
async def update_image_description(
    image_id: str,
    image_update_request: ChunkImageUpdateRequest,
    image_service: ImageService = Depends(Provide[Container.image_service]),
    user: User = Depends(get_current_user),
):
    try:
        image = await image_service.update_image(
            image_id,
            image_update_request.image_description,
            user.user_id,
        )
        return ChunkImageMapper.to_chunk_image_response(image)
    except HTTPException as e:
        logger.error(
            f"[Image] Image 설명 수정 중 오류 발생 : {user.user_id} -> {image_id}, detail: {e.detail}"
        )
        raise
    except Exception as e:
        logger.error(
            f"[Image] Image 설명 수정 중 오류 발생 : {user.user_id} -> {image_id}, detail: {str(e)}"
        )
        raise HTTPException(
            status_code=500,
            detail=f"Image 설명 수정 중 오류 발생: {str(e)}",
        )
