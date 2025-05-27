from chunks.domain.model.image_schema import ChunkImageSchema
from chunks.interface.dto.image_dto import ChunkImageResponse
from utils.object import get_str_id


class ChunkImageMapper:
    @staticmethod
    def to_chunk_image_response(
        chunk_image: ChunkImageSchema,
    ) -> ChunkImageResponse:
        return ChunkImageResponse(
            id=get_str_id(chunk_image.id),
            chunk_id=get_str_id(chunk_image.chunk_id),
            image_url=chunk_image.image_url,
            image_description=chunk_image.image_description,
        )
