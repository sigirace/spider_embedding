from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import UTC, datetime


class AppDetailRequest(BaseModel):
    """
    App 관련 메타 정보
    """

    description: Optional[str] = Field(default=None, description="APP 설명")
    keywords: Optional[List[str]] = Field(
        default_factory=list, description="APP 키워드 목록"
    )


class AppCreateRequest(AppDetailRequest):
    """
    App 생성 요청 모델
    """

    app_name: str = Field(..., description="APP ID, 4자리 대문자")


class AppResponse(BaseModel):
    id: str = Field(..., description="APP 고유 식별자")
    app_name: str = Field(..., description="APP ID, 4자리 대문자")
    description: Optional[str] = Field(default=None, description="APP 설명")
    keywords: Optional[List[str]] = Field(
        default_factory=list, description="APP 키워드 목록"
    )
    creator: str = Field(..., description="APP을 등록한 사용자 ID 또는 이름")
    updater: Optional[str] = Field(default=None, description="APP 수정자")
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC),
        description="생성 일시 (UTC, timezone-aware)",
    )
    updated_at: Optional[datetime] = Field(
        default=None,
        description="수정 일시 (UTC, timezone-aware)",
    )

    class Config:
        populate_by_name = True
