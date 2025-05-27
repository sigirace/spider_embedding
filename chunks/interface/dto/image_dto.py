from typing import Optional
from pydantic import BaseModel, Field


class ChunkImageResponse(BaseModel):
    id: str = Field(..., description="이미지 ID")
    chunk_id: str = Field(..., description="청크 ID")
    image_url: str = Field(..., description="이미지 URL")
    image_description: Optional[str] = Field(..., description="이미지 설명")


class ChunkImageUpdateRequest(BaseModel):
    image_description: Optional[str] = Field(..., description="이미지 설명")
