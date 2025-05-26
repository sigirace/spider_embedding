from typing import List, Optional
from bson import ObjectId
from pydantic import BaseModel, Field
from common.model import LifeCycle


class ChunkUpdateSchema(BaseModel):
    content: str = Field(..., description="청크 내용")
    tags: List[str] = Field(default=[], description="청크 태그")
    images: List[str] = Field(default=[], description="청크 이미지 리스트")


class ChunkDetail(ChunkUpdateSchema):
    page: int = Field(..., description="페이지 번호")
    file_creation_date: Optional[str] = Field(description="파일 생성 일시")
    file_mod_date: Optional[str] = Field(description="파일 수정 일시")


class ChunkSchema(ChunkDetail, LifeCycle):
    id: ObjectId = Field(default_factory=ObjectId, alias="_id")
    document_id: ObjectId = Field(..., description="문서 ID, 식별자")

    class Config:
        arbitrary_types_allowed = True
        populate_by_name = True


class ChunkParameterSchema(BaseModel):
    chunk_size: int = Field(default=250, description="청크 크기")
    chunk_overlap: int = Field(default=20, description="청크 중복")


class ChunkCreateSuccessSchema(BaseModel):
    document_id: ObjectId = Field(..., description="문서 ID")
    chunk_list: List[ChunkSchema] = Field(..., description="청크 리스트")

    class Config:
        arbitrary_types_allowed = True
        populate_by_name = True


class ChunkCreateErrorSchema(BaseModel):
    document_id: ObjectId = Field(..., description="문서 ID")
    error: str = Field(..., description="청크 생성 실패 이유")

    class Config:
        arbitrary_types_allowed = True
        populate_by_name = True


class ChunkBulkCreateSchema(BaseModel):
    success_document_list: List[ChunkCreateSuccessSchema] = Field(
        default=[], description="성공한 문서 리스트"
    )
    error_document_list: List[ChunkCreateErrorSchema] = Field(
        default=[], description="실패한 문서 리스트"
    )
