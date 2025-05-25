import os
from typing import List, Optional, Tuple
from fastapi import HTTPException, UploadFile
from app.application.app_service import AppService
from document.domain.model.document_schema import (
    DocumentDeleteSchema,
    DocumentErrorSchema,
    DocumentSchema,
    DocumentUpdateSchema,
)
from document.domain.repository.document_repository import IDocumentRepository
from utils.file_utils import (
    compute_file_hash,
    delete_file,
    rename_file,
    save_file,
)
from dependency_injector.wiring import inject

from utils.object import get_object_id, get_str_id


class DocumentService:

    @inject
    def __init__(
        self,
        app_service: AppService,
        document_repository: IDocumentRepository,
    ):
        self.app_service = app_service
        self.document_repository = document_repository

    async def create_document(
        self,
        app_id: str,
        file_list: List[UploadFile],
        user_id: str,
    ) -> Tuple[List[DocumentSchema], List[DocumentErrorSchema]]:
        """
        Document 생성
        """

        if not file_list:
            raise HTTPException(
                status_code=400,
                detail="업로드된 문서가 없습니다.",
            )

        existing_app = await self.app_service.get_app(app_id)

        success_list = []
        error_list = []

        for file in file_list:

            try:
                filename = file.filename or "No name"
                parts = filename.rsplit(".", 1)
                source = parts[-1] if len(parts) == 2 else "etc"

                hash = await compute_file_hash(file)

                existing_file = await self.document_repository.exist_document(
                    app_id=existing_app.id,
                    hash=hash,
                    size=file.size,
                )

                if existing_file:
                    raise HTTPException(
                        status_code=409,
                        detail="App에 이미 존재하는 문서입니다.",
                    )

                document = DocumentSchema(
                    name=filename,
                    hash=hash,
                    size=file.size,
                    type=file.content_type,
                    extension=source,
                    app_id=existing_app.id,
                    creator=user_id,
                )

                try:
                    file_path = await save_file(
                        file,
                        f"{existing_app.app_name}/{source}",
                    )  # APP/Source ex) TEST/pdf, TEST/excel, ...
                except OSError as e:
                    raise HTTPException(
                        status_code=500,
                        detail=f"파일 시스템 오류: {str(e)}",
                    )

                document.file_path = file_path
                document = await self.document_repository.create_document(document)
                success_list.append(document)

            except HTTPException as e:
                if e.status_code == 500:
                    raise

                if e.status_code == 409:
                    error_list.append(
                        DocumentErrorSchema(
                            name=file.filename,
                            error=str(e.detail),
                        )
                    )
                    continue

        return success_list, error_list

    async def get_document(
        self,
        document_id: str,
    ) -> DocumentSchema:
        """
        Document 조회
        """
        oid = get_object_id(document_id)
        document = await self.document_repository.get_document(oid)

        if not document:
            raise HTTPException(
                status_code=404,
                detail="문서가 존재하지 않습니다.",
            )

        return document

    async def get_document_list(
        self,
        app_id: str,
    ) -> List[DocumentSchema]:
        """
        Document 목록 조회
        """
        existing_app = await self.app_service.get_app(app_id)

        document_list = await self.document_repository.get_document_list(
            existing_app.id
        )

        if not document_list:
            raise HTTPException(
                status_code=404,
                detail="문서가 존재하지 않습니다.",
            )

        return document_list

    async def update_document(
        self,
        document_id: str,
        req: DocumentUpdateSchema,
        user_id: str,
    ) -> DocumentSchema:
        """
        Document 수정
        """

        document = await self.get_document(document_id)

        if not document:
            raise HTTPException(
                status_code=404,
                detail="문서가 존재하지 않습니다.",
            )

        if document.creator != user_id:
            raise HTTPException(
                status_code=403,
                detail="수정 권한이 없습니다.",
            )

        old_file_name = document.name
        new_file_name = req.name + "." + document.extension

        document.name = new_file_name
        document.updater = user_id

        try:
            file_path = os.path.dirname(document.file_path)

            new_file_path = rename_file(
                file_path=file_path,
                old_filename=old_file_name,
                new_filename=new_file_name,
            )
        except FileNotFoundError as e:
            raise HTTPException(
                status_code=404,
                detail=f"파일을 찾을 수 없습니다: {str(e)}",
            )

        document.file_path = new_file_path

        if await self.document_repository.update_document(document):
            return document
        else:
            raise HTTPException(
                status_code=500,
                detail="앱 정보 수정 실패",
            )

    async def delete_document(
        self,
        document_id: str,
        user_id: str,
    ) -> DocumentDeleteSchema:
        """
        Document 삭제
        """

        oid = get_object_id(document_id)
        document = await self.get_document(document_id)

        if not document:
            raise HTTPException(
                status_code=404,
                detail="문서가 존재하지 않습니다.",
            )

        if document.creator != user_id:
            raise HTTPException(
                status_code=403,
                detail="삭제 권한이 없습니다.",
            )

        try:
            delete_file(document.file_path)
        except FileNotFoundError as e:
            raise HTTPException(
                status_code=404,
                detail=f"파일을 찾을 수 없습니다: {str(e)}",
            )

        if await self.document_repository.delete_document(oid):
            return DocumentDeleteSchema(
                id=document_id,
                detail=f"문서 삭제 완료",
            )
        else:
            raise HTTPException(
                status_code=500,
                detail="문서 삭제 실패",
            )

    async def delete_document_list(
        self,
        app_id: str,
        document_list: Optional[List[str]],
        user_id: str,
    ) -> Tuple[List[DocumentDeleteSchema], List[DocumentErrorSchema]]:
        """
        Document 목록 삭제
        """

        existing_app = await self.app_service.get_app(app_id)

        if existing_app.creator != user_id:
            raise HTTPException(
                status_code=403,
                detail="삭제 권한이 없습니다.",
            )

        target_documents = (
            [
                get_str_id(doc.id)
                for doc in await self.get_document_list(get_str_id(existing_app.id))
            ]
            if not document_list
            else document_list
        )

        success_list: List[DocumentDeleteSchema] = []
        error_list: List[DocumentErrorSchema] = []

        for document_id in target_documents:
            try:

                delete_result = await self.delete_document(document_id, user_id)
                success_list.append(delete_result)

            except Exception as e:
                error_list.append(
                    DocumentErrorSchema(
                        name=document_id,
                        error=str(e),
                    )
                )
                continue

        return success_list, error_list
