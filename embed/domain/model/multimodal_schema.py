from pydantic import BaseModel, Field
from typing import List


class ImageDescription(BaseModel):
    summary: str = Field(..., description="이미지 요약")
    objects: List[str] = Field(..., description="주요 사물 리스트")
    text_elements: List[str] = Field(..., description="이미지 내 텍스트 요소")
    detail: str = Field(..., description="상세 설명")

    def __str__(self):
        objects_str = ", ".join(self.objects)
        text_elements_str = (
            ", ".join(self.text_elements) if self.text_elements else "없음"
        )
        return (
            f"이 이미지는 '{self.summary}' 장면을 담고 있습니다. "
            f"주요 사물로는 {objects_str}가 있으며, "
            f"이미지 내 텍스트는 {text_elements_str}입니다. "
            f"세부 묘사는 다음과 같습니다: {self.detail}"
        )
