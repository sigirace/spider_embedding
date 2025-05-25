from abc import ABC, abstractmethod

from meta.domain.model.meta_shcema import MetaSchema


class IMetaRepostory(ABC):

    @abstractmethod
    def create_meta(self, app_id: str, meta: MetaSchema) -> MetaSchema:
        pass

    @abstractmethod
    def get_meta(self, app_id: str, meta_id: str) -> MetaSchema:
        pass

    @abstractmethod
    def update_meta(self, app_id: str, meta: MetaSchema) -> bool:
        pass

    @abstractmethod
    def delete_meta(self, app_id: str, meta_id: str) -> bool:
        pass
