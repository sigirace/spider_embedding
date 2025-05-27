from dependency_injector import containers, providers

from app.application.app_service import AppService

from app.infra.app_repository_impl import AppRepository
from chunks.application.chunk_service import ChunkService
from chunks.application.image_service import ImageService
from chunks.infra.chunk_repository_impl import ChunkRepository
from chunks.infra.image_repository_impl import ImageRepository
from database.mongo import get_async_mongo_client
from document.application.document_service import DocumentService
from document.infra.document_repository_impl import DocumentRepository
from llm.application.llm_service import LLMService
from llm.infra.repository.llm_repository_impl import HaiqvLLMRepository
from user.application.token_service import TokenService


class Container(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(
        packages=[
            "user",
            "app",
            "document",
            "chunks",
            "llm",
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

    chunk_repository = providers.Factory(
        ChunkRepository,
        mongo_client,
    )

    image_repository = providers.Factory(
        ImageRepository,
        mongo_client,
    )

    image_service = providers.Factory(
        ImageService,
        image_repository=image_repository,
        chunk_repository=chunk_repository,
    )

    chunk_service = providers.Factory(
        ChunkService,
        app_service=app_service,
        document_service=document_service,
        image_service=image_service,
        chunk_repository=chunk_repository,
    )

    llm_repository = providers.Singleton(HaiqvLLMRepository)

    llm_service = providers.Factory(
        LLMService,
        llm_repository=llm_repository,
    )
