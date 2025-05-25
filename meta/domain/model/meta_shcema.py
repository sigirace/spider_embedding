from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import UTC, datetime


class MetaSchema(BaseModel):
    hash_id: Optional[str] = Field(
        default=None,
        description="파일의 고유 식별자(hash+size 기반)",
    )  # 파일 중복 검사 여부를 위함
    app_id: str = Field(..., description="파일이 속한 앱의 고유 ID")
    name: str = Field(..., description="파일 이름 (예: report.pdf)")
    hash: str = Field(..., description="파일의 해시값 (무결성 검사용)")
    size: int = Field(..., description="파일 크기 (단위: 바이트)")
    file_path: str = Field(
        default_factory=lambda: "", description="파일이 저장된 경로 또는 URL"
    )
    chunks: List[str] = Field(default=[], description="파일에 포함된 청크 목록")
    type: str = Field(..., description="파일의 유형 (예: document, image)")
    extension: str = Field(..., description="파일 확장자 (예: pdf, jpg)")
    creator: str = Field(..., description="파일을 업로드한 사용자 ID 또는 이름")
    created_at: Optional[datetime] = Field(
        default_factory=lambda: datetime.now(UTC),
        description="생성 일시 (UTC, timezone-aware)",
    )
    updated_at: Optional[datetime] = Field(
        default=None,
        description="수정 일시 (UTC, timezone-aware)",
    )

    def model_post_init(self, __context) -> None:
        # id가 지정되지 않은 경우, hash+size 조합으로 생성
        if not self.id:
            self.hash_id = f"{self.hash}_{self.size}"
