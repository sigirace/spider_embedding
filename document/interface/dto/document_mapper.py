from typing import List
from document.domain.model.document_schema import (
    DocumentDeleteSchema,
    DocumentErrorSchema,
    DocumentSchema,
    DocumentUpdateSchema,
)
from document.interface.dto.document_dto import (
    DocumentDeleteListResponse,
    DocumentDeleteResponse,
    DocumentErrorResponse,
    DocumentListResponse,
    DocumentResponse,
    DocumentUpdateRequest,
)
from utils.object import get_str_id


class DocumentMapper:
    @staticmethod
    def to_document_response(document: DocumentSchema) -> DocumentResponse:
        return DocumentResponse(
            id=get_str_id(document.id),
            app_id=get_str_id(document.app_id),
            name=document.name,
            hash=document.hash,
            size=document.size,
            file_path=document.file_path,
            type=document.type,
            extension=document.extension,
            creator=document.creator,
            updater=document.updater,
            created_at=document.created_at,
            updated_at=document.updated_at,
        )

    @staticmethod
    def to_document_error_response(error: DocumentErrorSchema) -> DocumentErrorResponse:
        return DocumentErrorResponse(
            name=error.name,
            error=error.error,
        )

    @staticmethod
    def to_document_list_response(
        success_list: List[DocumentSchema],
        error_list: List[DocumentErrorSchema],
    ) -> DocumentListResponse:
        return DocumentListResponse(
            success_list=[
                DocumentMapper.to_document_response(document)
                for document in success_list
            ],
            error_list=[
                DocumentMapper.to_document_error_response(error) for error in error_list
            ],
        )

    @staticmethod
    def to_document_update_schema(req: DocumentUpdateRequest) -> DocumentUpdateSchema:
        return DocumentUpdateSchema(
            name=req.name,
        )

    @staticmethod
    def to_document_delete_response(
        delete_result: DocumentDeleteSchema,
    ) -> DocumentDeleteResponse:
        return DocumentDeleteResponse(
            id=delete_result.id,
            detail=delete_result.detail,
        )

    @staticmethod
    def to_document_delete_list_response(
        success_list: List[DocumentDeleteSchema],
        error_list: List[DocumentErrorSchema],
    ) -> DocumentDeleteListResponse:
        return DocumentDeleteListResponse(
            success_list=[
                DocumentMapper.to_document_delete_response(delete_result)
                for delete_result in success_list
            ],
            error_list=[
                DocumentMapper.to_document_error_response(error) for error in error_list
            ],
        )
