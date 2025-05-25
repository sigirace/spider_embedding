from typing import List
from fastapi import HTTPException
from app.domain.model.app_schema import AppDetail, AppSchema
from app.domain.repository.app_repository import IAppRepository

from utils.file_utils import (
    create_folder,
    delete_folder,
)
from dependency_injector.wiring import inject

from utils.object import get_object_id


class AppService:

    @inject
    def __init__(
        self,
        app_repository: IAppRepository,
    ):
        self.app_repository = app_repository

    async def create_app(
        self,
        app_schema: AppSchema,
    ) -> AppSchema:
        """
        App 생성
        """

        existing = await self.app_repository.get_app_by_app_name(app_schema.app_name)

        if existing:
            raise HTTPException(
                status_code=409,
                detail="이미 존재하는 App ID입니다.",
            )

        app = await self.app_repository.create_app(app_schema)

        try:
            if not create_folder(app_schema.app_name):
                await self.app_repository.delete_app(app.id)  # 롤백
                raise HTTPException(
                    status_code=500,
                    detail="앱 폴더 생성 실패",
                )
        except OSError as e:
            raise HTTPException(status_code=500, detail=f"파일 시스템 오류: {str(e)}")

        return app

    async def get_app(
        self,
        id: str,
    ) -> AppSchema:
        """
        App 정보 조회
        """

        oid = get_object_id(id)
        app = await self.app_repository.get_app(oid)

        if not app:
            raise HTTPException(
                status_code=404,
                detail="App이 존재하지 않습니다.",
            )

        return app

    async def get_app_list(
        self,
        user_id: str,
    ) -> List[AppSchema]:
        """
        User ID 기반으로 App 목록 조회
        """
        return await self.app_repository.get_app_list(user_id)

    async def update_app(
        self,
        id: str,
        req: AppDetail,
        user_id: str,
    ) -> AppSchema:
        """
        App 정보 수정
        """

        app: AppSchema = await self.get_app(id)

        if app.creator != user_id:
            # 앱은 생성자만 수정 가능
            raise HTTPException(
                status_code=403,
                detail="수정 권한이 없습니다.",
            )

        app.description = req.description
        app.keywords = req.keywords
        app.updater = user_id

        if await self.app_repository.update_app(app):
            return app
        else:
            raise HTTPException(
                status_code=500,
                detail="앱 정보 수정 실패",
            )

    async def delete_app(
        self,
        user_id: str,
        id: str,
    ) -> bool:
        """
        App 삭제
        """

        oid = get_object_id(id)
        app = await self.get_app(oid)

        if app.creator != user_id:
            # 앱은 생성자만 삭제 가능
            raise HTTPException(
                status_code=403,
                detail="삭제 권한이 없습니다.",
            )

        try:
            if not delete_folder(app.app_name):
                raise HTTPException(
                    status_code=500,
                    detail="앱 폴더 삭제 실패",
                )

            ## 벡터디비 삭제 기능 필요
        except OSError as e:
            raise HTTPException(status_code=500, detail=f"파일 시스템 오류: {str(e)}")

        return await self.app_repository.delete_app(oid)
