from abc import ABC, abstractmethod
from typing import List, Optional

from bson import ObjectId

from app.domain.model.app_schema import AppSchema


class IAppRepository(ABC):

    @abstractmethod
    async def create_app(self, app: AppSchema) -> AppSchema:
        """
        AppSchema 기반으로 App 생성
        """
        pass

    @abstractmethod
    async def get_app(self, id: ObjectId) -> Optional[AppSchema]:
        """
        Mongo DB의 ID 기반으로 App 조회
        """
        pass

    @abstractmethod
    async def get_app_by_app_name(self, app_name: str) -> Optional[AppSchema]:
        """
        App ID 기반으로 App 조회
        """
        pass

    @abstractmethod
    async def get_app_list(self, user_id: str) -> List[AppSchema]:
        """
        User ID 기반으로 App 목록 조회
        """
        pass

    @abstractmethod
    async def update_app(self, app: AppSchema) -> bool:
        """
        AppSchema 기반으로 App 정보 수정
        대상 App은 Mongo DB의 ID 기반으로 조회
        """
        pass

    @abstractmethod
    async def delete_app(self, id: ObjectId) -> bool:
        """
        Mongo DB의 ID 기반으로 App 삭제
        """
        pass
