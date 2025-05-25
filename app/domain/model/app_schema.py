import re
from bson import ObjectId
from pydantic import BaseModel, Field, field_validator
from typing import List, Optional
from common.model import LifeCycle


class AppDetail(BaseModel):
    description: Optional[str] = Field(default=None, description="APP 설명")
    keywords: Optional[List[str]] = Field(default=[], description="APP 키워드 목록")


class AppSchema(AppDetail, LifeCycle):
    id: ObjectId = Field(default_factory=ObjectId, alias="_id")
    app_name: str = Field(..., description="APP ID (대문자 4자리)")

    @field_validator("app_name")
    @classmethod
    def validate_app_name_format(cls, v: str) -> str:
        if not re.fullmatch(r"^[A-Z]{4}$", v):
            raise ValueError("app_name는 대문자 4글자여야 합니다 (예: 'ABCD')")
        return v

    class Config:
        arbitrary_types_allowed = True
        populate_by_name = True
