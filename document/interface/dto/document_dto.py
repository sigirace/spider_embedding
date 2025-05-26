from datetime import UTC, datetime
from typing import List, Optional
from pydantic import BaseModel, Field
from common.dto import LifeCycleResponse


class DocumentResponse(LifeCycleResponse):
    id: str = Field(..., description="문서 ID, 식별자")
    app_id: str = Field(..., description="APP ID, 식별자")
    name: str = Field(..., description="문서 이름")
    hash: str = Field(..., description="문서 해시값")
    size: int = Field(..., description="문서 크기")
    file_path: str = Field(..., description="문서 경로")
    type: str = Field(..., description="문서 타입")
    extension: str = Field(..., description="문서 확장자")

    class Config:
        populate_by_name = True


class DocumentErrorResponse(BaseModel):
    name: str = Field(..., description="문서 이름")
    error: str = Field(..., description="문서 생성 실패 이유")


class DocumentListResponse(BaseModel):
    success_list: List[DocumentResponse] = Field(
        ..., description="업로드 성공한 문서 목록"
    )
    error_list: List[DocumentErrorResponse] = Field(
        ..., description="업로드 실패한 문서 목록"
    )


class DocumentUpdateRequest(BaseModel):
    name: str = Field(..., description="문서 이름")


class DocumentDeleteResponse(BaseModel):
    id: str = Field(..., description="문서 ID")
    detail: Optional[str] = Field(default=None, description="문서 삭제 상세 정보")


class DocumentDeleteListRequest(BaseModel):
    document_list: Optional[List[str]] = Field(default=None, description="문서 목록")


class DocumentDeleteListResponse(BaseModel):
    success_list: List[DocumentDeleteResponse] = Field(
        ..., description="삭제에 성공한 문서 목록"
    )
    error_list: List[DocumentErrorResponse] = Field(
        ..., description="삭제에 실패한 문서 목록"
    )
