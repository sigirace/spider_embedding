from abc import ABC, abstractmethod
from typing import List, Optional

from bson import ObjectId

from document.domain.model.document_schema import DocumentSchema


class IDocumentRepository(ABC):

    @abstractmethod
    async def create_document(self, document: DocumentSchema) -> DocumentSchema:
        """
        DocumentSchema 기반으로 Document 생성
        """
        pass

    @abstractmethod
    async def exist_document(self, app_id: str, hash: str, size: int) -> bool:
        """
        App ID, Hash, Size 기반으로 Document 존재 여부 확인
        Hash와 Size는 App 내에서 문서의 식별자 역할을 함
        """
        pass

    @abstractmethod
    async def get_document(self, document_id: ObjectId) -> Optional[DocumentSchema]:
        """
        Document ID 기반으로 Document 조회
        """
        pass

    @abstractmethod
    async def get_document_list(self, app_id: ObjectId) -> List[DocumentSchema]:
        """
        App ID 기반으로 Document 목록 조회
        """
        pass

    @abstractmethod
    async def update_document(self, document: DocumentSchema) -> bool:
        """
        Document 수정
        """
        pass

    @abstractmethod
    async def delete_document(self, document_id: ObjectId) -> bool:
        """
        Document 삭제
        """
        pass
