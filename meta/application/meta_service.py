async def get_meta(self, app_id: str, meta_id: str) -> MetaSchema:

    app = await self.get_app(app_id)

    meta = next((m for m in app.metadata if m.id == meta_id), None)

    if not meta:
        raise HTTPException(
            status_code=404,
            detail="Meta not found",
        )

    return meta


async def get_meta_list(self, app_id: str) -> list[MetaSchema]:

    app = await self.get_app(app_id)

    meta_list = app.metadata

    return meta_list


async def create_meta(
    self,
    app_id: str,
    files: list[UploadFile],
    user_id: str,
) -> tuple[list[MetaSchema], list[dict]]:

    await self.get_app(app_id)

    file_list = []
    error_list = []

    for file in files:
        try:

            filename = file.filename or "No name"
            parts = filename.rsplit(".", 1)
            source = parts[-1] if len(parts) == 2 else "etc"

            hash = await compute_file_hash(file)

            meta = MetaSchema(
                name=filename,
                hash=hash,
                size=file.size,
                type=file.content_type,
                extension=source,
                creator=user_id,
            )

            try:
                await self.get_meta(app_id, meta.id)
                raise ValueError(f"파일 {meta.name}은 이미 존재합니다.")
            except HTTPException as e:
                if e.status_code != 404:
                    raise

            # 메타 파일이 없을때만 저장
            file_path = await save_file(
                file=file,
                file_path=f"{app_id}/{source}",  # ABCD/pdf
            )  # ./data/app_id/source/file_name.ext

            meta.file_path = file_path

            meta: MetaSchema = await self.app_repository.create_meta(app_id, meta)

            file_list.append(meta)

        except Exception as e:

            error_list.append(
                {
                    "name": file.filename,
                    "error": str(e),
                }
            )
            continue

    return file_list, error_list


async def delete_meta(self, app_id: str, meta_id: str, user_id: str) -> bool:

    app = await self.get_app(app_id)

    meta = next((m for m in app.metadata if m.id == meta_id), None)

    if not meta:
        raise HTTPException(
            status_code=404,
            detail="Meta not found",
        )

    if app.creator != user_id and meta.creator != user_id:
        # 둘 중 하나만 만족해도 삭제 권한 있다고 판단
        raise HTTPException(
            status_code=403,
            detail="삭제 권한이 없습니다.",
        )

    delete_file(meta.file_path)
    img_save_path = f"{app_id}/{meta_id}"
    delete_image_folder(img_save_path)

    ## 벡터디비 삭제 기능 필요

    return await self.app_repository.delete_meta(app_id, meta_id)


async def update_meta(
    self,
    app_id: str,
    meta_id: str,
    user_id: str,
    name: Optional[str] = None,
) -> MetaSchema:

    app = await self.get_app(app_id)
    meta = next((m for m in app.metadata if m.id == meta_id), None)

    if not meta:
        raise HTTPException(
            status_code=404,
            detail="Meta not found",
        )

    if app.creator != user_id and meta.creator != user_id:
        # 둘 중 하나만 만족해도 수정 권한 있다고 판단
        raise HTTPException(
            status_code=403,
            detail="수정 권한이 없습니다.",
        )

    if name:
        meta.name = name

    await self.app_repository.update_meta(app_id, meta)

    return meta
