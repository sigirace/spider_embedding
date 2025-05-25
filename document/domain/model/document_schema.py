from typing import Optional
from bson import ObjectId
from pydantic import BaseModel, Field
from common.model import LifeCycle


class DocumentUpdateSchema(BaseModel):
    name: str = Field(..., description="문서 이름")


class DocumentDetail(DocumentUpdateSchema):
    hash: str = Field(..., description="파일의 해시값 (무결성 검사용)")
    size: int = Field(..., description="파일 크기 (단위: 바이트)")
    file_path: str = Field(
        default_factory=lambda: "", description="파일이 저장된 경로 또는 URL"
    )
    type: str = Field(..., description="파일의 유형 (예: document, image)")
    extension: str = Field(..., description="파일 확장자 (예: pdf, jpg)")


class DocumentSchema(DocumentDetail, LifeCycle):
    id: ObjectId = Field(default_factory=ObjectId, alias="_id")
    app_id: ObjectId = Field(..., description="APP ID, 식별자")

    class Config:
        arbitrary_types_allowed = True
        populate_by_name = True


class DocumentErrorSchema(BaseModel):
    name: str = Field(..., description="문서 이름")
    error: str = Field(..., description="문서 생성 실패 이유")


class DocumentDeleteSchema(BaseModel):
    id: str = Field(..., description="문서 ID")
    detail: Optional[str] = Field(default=None, description="문서 삭제 상세 정보")
