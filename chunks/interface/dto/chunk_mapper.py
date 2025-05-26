from chunks.domain.model.chunk_schema import (
    ChunkBulkCreateSchema,
    ChunkCreateErrorSchema,
    ChunkCreateSuccessSchema,
    ChunkParameterSchema,
    ChunkSchema,
)
from chunks.interface.dto.chunk_dto import (
    ChunkBulkCreateResponse,
    ChunkCreateErrorResponse,
    ChunkCreateSuccessResponse,
    ChunkParameterRequest,
    ChunkResponse,
)
from utils.object import get_str_id


class ChunkMapper:
    @staticmethod
    def to_chunk_parameter_schema(
        request: ChunkParameterRequest,
    ) -> ChunkParameterSchema:
        return ChunkParameterSchema(
            chunk_size=request.chunk_size,
            chunk_overlap=request.chunk_overlap,
        )

    @staticmethod
    def to_chunk_response(
        chunk: ChunkSchema,
    ) -> ChunkResponse:
        return ChunkResponse(
            id=get_str_id(chunk.id),
            document_id=get_str_id(chunk.document_id),
            content=chunk.content,
            tags=chunk.tags,
            images=chunk.images,
            page=chunk.page,
            file_creation_date=chunk.file_creation_date,
            file_mod_date=chunk.file_mod_date,
            creator=chunk.creator,
            updater=chunk.updater,
            created_at=chunk.created_at,
            updated_at=chunk.updated_at,
        )

    @staticmethod
    def to_chunk_create_success_response(
        chunk_create_success_schema: ChunkCreateSuccessSchema,
    ) -> ChunkCreateSuccessResponse:
        return ChunkCreateSuccessResponse(
            document_id=get_str_id(chunk_create_success_schema.document_id),
            chunk_list=[
                ChunkMapper.to_chunk_response(chunk)
                for chunk in chunk_create_success_schema.chunk_list
            ],
        )

    @staticmethod
    def to_chunk_create_error_response(
        chunk_create_error_schema: ChunkCreateErrorSchema,
    ) -> ChunkCreateErrorResponse:
        return ChunkCreateErrorResponse(
            document_id=get_str_id(chunk_create_error_schema.document_id),
            error=chunk_create_error_schema.error,
        )

    @staticmethod
    def to_chunk_bulk_create_response(
        chunk_bulk_create_schema: ChunkBulkCreateSchema,
    ) -> ChunkBulkCreateResponse:
        return ChunkBulkCreateResponse(
            success_document_list=[
                ChunkMapper.to_chunk_create_success_response(schema)
                for schema in chunk_bulk_create_schema.success_document_list
            ],
            error_document_list=[
                ChunkMapper.to_chunk_create_error_response(schema)
                for schema in chunk_bulk_create_schema.error_document_list
            ],
        )
