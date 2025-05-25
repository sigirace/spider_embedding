class ChunkResponse(BaseModel):
    id: str = Field(..., description="청크 고유 식별자")  # Mongodb ObjectID
    page: int = Field(..., description="페이지 번호")
    tags: List[str] = Field(..., description="페이지에 포함된 태그 목록")
    images: List[str] = Field(
        default=[], description="페이지에 포함된 이미지 경로 목록"
    )
    content: str = Field(..., description="페이지 텍스트")
    # embed_state: bool = Field(
    #     default=False,
    #     description="청크 임베딩 상태 (True: 임베딩 완료, False: 임베딩 미완료)",
    # )
    # created_at: datetime = Field(
    #     default_factory=lambda: datetime.now(UTC),
    #     description="생성 일시 (UTC, timezone-aware)",
    # )
    # updated_at: Optional[datetime] = Field(
    #     default=None,
    #     description="수정 일시 (UTC, timezone-aware)",
    # )
    # creator: str = Field(..., description="청크 생성자")
    # updater: Optional[str] = Field(default=None, description="청크 수정자")


class MetaResponse(BaseModel):
    id: str = Field(
        ..., description="파일의 고유 식별자(hash+size 기반)"
    )  # 파일 중복 검사를 위함
    name: str = Field(..., description="파일 이름 (예: report.pdf)")
    chunks: List[ChunkResponse] = Field(
        default=[], description="파일에 포함된 청크 목록"
    )
    creator: str = Field(..., description="파일을 업로드한 사용자 ID 또는 이름")
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC),
        description="생성 일시 (UTC, timezone-aware)",
    )
    updated_at: Optional[datetime] = Field(
        default=None,
        description="수정 일시 (UTC, timezone-aware)",
    )


class MetaRequest(BaseModel):
    app_id: str = Field(..., description="APP 고유 ID")
    meta_id: str = Field(..., description="메타 고유 ID")
    name: str = Field(..., description="메타 이름")


class MetaUploadResponse(BaseModel):
    uploaded_list: List[MetaResponse] = Field(..., description="업로드된 메타 목록")
    error_list: List[dict] = Field(..., description="업로드 오류 목록")
