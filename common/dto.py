from datetime import UTC, datetime
from fastapi.responses import JSONResponse
from typing import Any, Optional

from pydantic import BaseModel, Field


class CommonResponse(JSONResponse):
    def __init__(
        self,
        message: str = "요청이 성공적으로 처리되었습니다.",
        data: Any = None,
        status_code: int = 200,
    ):
        content = {
            "status": "success",
            "message": message,
            "data": data,
        }
        super().__init__(status_code=status_code, content=content)


class LifeCycleResponse(BaseModel):
    creator: str = Field(..., description="생성자 ID")
    updater: Optional[str] = Field(default=None, description="수정자")
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC),
        description="생성 일시 (UTC, timezone-aware)",
    )
    updated_at: Optional[datetime] = Field(
        default=None,
        description="수정 일시 (UTC, timezone-aware)",
    )
