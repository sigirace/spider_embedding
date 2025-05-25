from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import UTC, datetime


class ChunkSchema(BaseModel):
    id: str = Field(
        default_factory=lambda: str(PyObjectId()),
        description="청크의 고유 식별자",
    )  # Mongodb ObjectID
    page: int = Field(..., description="페이지 번호")
    tags: List[str] = Field(..., description="페이지에 포함된 태그 목록")
    images: List[str] = Field(
        default=[], description="페이지에 포함된 이미지 경로 목록"
    )
    content: str = Field(..., description="페이지 텍스트")
    embed_state: bool = Field(
        default=False,
        description="청크 임베딩 상태 (True: 임베딩 완료, False: 임베딩 미완료)",
    )
    file_creation_date: Optional[str] = Field(description="파일 생성 일시")
    file_mod_date: Optional[str] = Field(description="파일 수정 일시")
    created_at: Optional[datetime] = Field(
        default_factory=lambda: datetime.now(UTC),
        description="생성 일시 (UTC, timezone-aware)",
    )
    updated_at: Optional[datetime] = Field(
        default=None,
        description="수정 일시 (UTC, timezone-aware)",
    )
    creator: str = Field(..., description="청크 생성자")
    updater: Optional[str] = Field(default=None, description="청크 수정자")
