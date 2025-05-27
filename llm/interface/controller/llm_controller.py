from fastapi import APIRouter, Depends
from dependency_injector.wiring import Provide, inject

from containers import Container
from llm.application.llm_service import LLMService
from llm.interface.dto.llm_dto import ChatRequest, ChatResponse

router = APIRouter(prefix="/llm")


@router.post("/invoke")
@inject
async def invoke(
    req: ChatRequest,
    llm_service: LLMService = Depends(Provide[Container.llm_service]),
):
    content = llm_service.chat(req.messages)
    return ChatResponse(content=content)
