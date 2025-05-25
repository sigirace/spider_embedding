from fastapi.responses import JSONResponse
from typing import Any


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
