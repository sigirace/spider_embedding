from dependency_injector import containers, providers

from app.application.app_service import AppService

from app.infra.app_repository_impl import AppRepository
from database.mongo import get_async_mongo_client
from document.application.document_service import DocumentService
from document.infra.document_repository_impl import DocumentRepository
from user.application.token_service import TokenService


class Container(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(
        packages=[
            "user",
            "app",
            "document",
        ],
    )

    mongo_client = providers.Singleton(get_async_mongo_client)

    app_repository = providers.Factory(
        AppRepository,
        mongo_client,
    )

    app_service = providers.Factory(
        AppService,
        app_repository=app_repository,
    )

    token_service = providers.Factory(
        TokenService,
    )

    document_repository = providers.Factory(
        DocumentRepository,
        mongo_client,
    )

    document_service = providers.Factory(
        DocumentService,
        app_service=app_service,
        document_repository=document_repository,
    )
