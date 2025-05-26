from typing import List, Optional
from pydantic import BaseModel, Field
from common.dto import LifeCycleResponse


class ChunkParameterRequest(BaseModel):
    chunk_size: int = Field(default=250, description="청크 크기")
    chunk_overlap: int = Field(default=20, description="청크 중복")


class ChunkResponse(LifeCycleResponse):
    id: str = Field(..., description="청크 ID")
    document_id: str = Field(..., description="문서 ID")
    content: str = Field(..., description="청크 내용")
    tags: List[str] = Field(default=[], description="청크 태그")
    images: List[str] = Field(default=[], description="청크 이미지 리스트")
    page: int = Field(..., description="페이지 번호")
    file_creation_date: Optional[str] = Field(description="파일 생성 일시")
    file_mod_date: Optional[str] = Field(description="파일 수정 일시")

    class Config:
        populate_by_name = True


class ChunkCreateSuccessResponse(BaseModel):
    document_id: str = Field(..., description="문서 ID")
    chunk_list: List[ChunkResponse] = Field(..., description="청크 리스트")


class ChunkCreateErrorResponse(BaseModel):
    document_id: str = Field(..., description="문서 ID")
    error: str = Field(..., description="청크 생성 실패 이유")


class ChunkBulkCreateResponse(BaseModel):
    success_document_list: List[ChunkCreateSuccessResponse] = Field(
        default=[], description="성공한 문서 리스트"
    )
    error_document_list: List[ChunkCreateErrorResponse] = Field(
        default=[], description="실패한 문서 리스트"
    )
