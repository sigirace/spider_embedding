from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field


class ChunkAllRequest(BaseModel):
    app_id: str = Field(..., description="앱 ID")
    chunk_size: Optional[int] = Field(default=500, description="청크 크기")
    chunk_overlap: Optional[int] = Field(default=50, description="청크 중복 크기")


class ChunkRequest(ChunkAllRequest):
    meta_id: Optional[str] = Field(default=None, description="메타 ID")


class ChunkResponse(BaseModel):
    id: str = Field(..., description="청크 ID")
    page: int = Field(..., description="페이지 번호")
    tags: List[str] = Field(..., description="페이지에 포함된 태그 목록")
    images: List[str] = Field(..., description="페이지에 포함된 이미지 경로 목록")
    content: str = Field(..., description="페이지 텍스트")
    embed_state: bool = Field(..., description="청크 임베딩 상태")
    creator: str = Field(..., description="청크 생성자")
    updater: Optional[str] = Field(default=None, description="청크 수정자")
    created_at: datetime = Field(..., description="청크 생성 일시")
    updated_at: Optional[datetime] = Field(default=None, description="청크 수정 일시")


class ChunkAllResponse(BaseModel):
    success_list: List[str] = Field(..., description="성공한 메타 ID 목록")
    error_list: List[dict] = Field(..., description="실패한 메타 ID 목록")
