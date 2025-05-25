from bson import ObjectId
from app.domain.model.app_schema import AppDetail, AppSchema
from app.interface.dto.app_dto import (
    AppCreateRequest,
    AppDetailRequest,
    AppResponse,
)
from utils.object import get_str_id


class AppMapper:

    @staticmethod
    def to_app_create_schema(dto: AppCreateRequest, creator: str) -> AppSchema:
        return AppSchema(
            id=ObjectId(),
            app_name=dto.app_name,
            description=dto.description,
            keywords=dto.keywords,
            creator=creator,
        )

    @staticmethod
    def to_app_detail_schema(dto: AppDetailRequest) -> AppDetail:
        return AppDetail(
            description=dto.description,
            keywords=dto.keywords,
        )

    @staticmethod
    def to_app_response(app: AppSchema) -> AppResponse:
        return AppResponse(
            id=get_str_id(app.id),
            app_name=app.app_name,
            description=app.description,
            keywords=app.keywords,
            creator=app.creator,
            updater=app.updater,
            created_at=app.created_at,
            updated_at=app.updated_at,
        )
