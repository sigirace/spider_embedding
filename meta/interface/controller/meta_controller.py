@router.get("/{app_id}/meta/{meta_id}")
@inject
async def get_meta(
    app_id: str,
    meta_id: str,
    app_service: AppService = Depends(Provide[Container.app_service]),
    user: User = Depends(get_current_user),
):
    try:
        logger.info(f"[App] {user.user_id}: {app_id} 메타 정보 요청")
        meta = await app_service.get_meta(
            app_id=app_id,
            meta_id=meta_id,
        )
        logger.info(f"[App] {user.user_id}: {app_id} 메타 정보 요청 완료")
        return MetaResponse(**meta.model_dump())
    except Exception as e:
        logger.error(
            f"[App] {user.user_id}: {app_id} 메타 정보 조회 실패, detail: {str(e)}"
        )
        raise


@router.get("/{app_id}/meta")
@inject
async def get_meta_list(
    app_id: str,
    app_service: AppService = Depends(Provide[Container.app_service]),
    user: User = Depends(get_current_user),
):
    try:
        logger.info(f"[App] {user.user_id}: {app_id} 메타 정보 목록 요청")
        meta_list = await app_service.get_meta_list(app_id)
        logger.info(f"[App] {user.user_id}: {app_id} 메타 정보 목록 요청 완료")
        return [MetaResponse(**m.model_dump()) for m in meta_list]
    except Exception as e:
        logger.error(
            f"[App] {user.user_id}: {app_id} 메타 정보 목록 조회 실패, detail: {str(e)}"
        )
        raise


@router.post("/{app_id}/meta")
@inject
async def create_meta(
    app_id: str,
    files: List[UploadFile] = File(default=None),
    app_service: AppService = Depends(Provide[Container.app_service]),
    user: User = Depends(get_current_user),
):
    try:
        logger.info(f"[App] {app_id} 메타 파일 업로드")

        if not files:
            logger.error(
                f"[App] {app_id} 메타 파일 업로드 실패, detail: 업로드된 파일이 없습니다."
            )
            raise HTTPException(status_code=400, detail="업로드된 파일이 없습니다.")

        meta_list, error_list = await app_service.create_meta(
            app_id=app_id,
            files=files,
            user_id=user.user_id,
        )

        logger.info(f"[App] {app_id} 메타 파일 업로드 완료")

        return MetaUploadResponse(
            uploaded_list=[MetaResponse(**m.model_dump()) for m in meta_list],
            error_list=error_list,
        )
    except Exception as e:
        logger.error(f"[App] {app_id} 메타 파일 업로드 실패, detail: {str(e)}")
        raise


@router.delete("/{app_id}/meta/{meta_id}")
@inject
async def delete_meta(
    app_id: str,
    meta_id: str,
    app_service: AppService = Depends(Provide[Container.app_service]),
    user: User = Depends(get_current_user),
):
    try:
        logger.info(f"[App] {user.user_id}: {app_id} 메타 정보 삭제")
        await app_service.delete_meta(
            app_id=app_id,
            meta_id=meta_id,
            user_id=user.user_id,
        )
        logger.info(f"[App] {user.user_id}: {app_id} 메타 정보 삭제 완료")
        return JSONResponse(
            status_code=200,
            content={"message": f"{app_id} - {meta_id} 메타 정보 삭제 완료"},
        )
    except ValueError as e:
        logger.error(
            f"[App] {user.user_id}: {app_id} 메타 정보 삭제 실패, detail: {str(e)}"
        )
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(
            f"[App] {user.user_id}: {app_id} 메타 정보 삭제 실패, detail: {str(e)}"
        )
        raise


@router.put("/{app_id}/meta/{meta_id}")
@inject
async def update_meta(
    meta_req: MetaRequest,
    app_service: AppService = Depends(Provide[Container.app_service]),
    user: User = Depends(get_current_user),
):
    try:
        logger.info(f"[App] {user.user_id}: {meta_req.app_id} 메타 정보 수정")
        meta = await app_service.update_meta(
            app_id=meta_req.app_id,
            meta_id=meta_req.meta_id,
            name=meta_req.name,
            user_id=user.user_id,
        )
        logger.info(f"[App] {user.user_id}: {meta_req.app_id} 메타 정보 수정 완료")
        return MetaResponse(**meta.model_dump())
    except Exception as e:
        logger.error(
            f"[App] {user.user_id}: {meta_req.app_id} 메타 정보 수정 실패, detail: {str(e)}"
        )
        raise
