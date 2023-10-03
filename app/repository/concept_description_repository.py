from abc import abstractmethod
from base64 import urlsafe_b64decode, urlsafe_b64encode
from typing import List, Union

from app.models.concept_description import ConceptDescription
from app.models.response import GetConceptDescriptionsResult, Result, RepositoryMetadata


def base_64_url_encode(data: str) -> str:
    return urlsafe_b64encode(data.encode('utf-8')).rstrip(b"=").decode('utf-8')


def base_64_url_decode(base_64_url: str) -> str:
    return urlsafe_b64decode(base_64_url + '=' * (4 - len(base_64_url) % 4)).decode('utf-8')


class ConceptDescriptionRepository(object):

    @abstractmethod
    async def connect_to_database(self, db_setting: dict):
        pass

    @abstractmethod
    async def close_database_connection(self):
        pass

    @abstractmethod
    async def get_concept_descriptions(self, query: dict, cursor=None, limit=100) -> GetConceptDescriptionsResult:
        pass

    @abstractmethod
    async def get_concept_description(self, cd_id_base64url_encoded: str) -> ConceptDescription:
        pass

    @abstractmethod
    async def add_concept_description(self, concept_description: ConceptDescription) -> ConceptDescription:
        pass

    @abstractmethod
    async def update_concept_description(
            self, cd_id_base64url_encoded: str, concept_description: ConceptDescription
    ) -> bool:
        pass

    @abstractmethod
    async def delete_concept_description(self, cd_id_base64url_encoded: str) -> bool:
        pass

    def get_repository_metadata(self) -> RepositoryMetadata:
        pass

    @abstractmethod
    async def get_concept_description_history(
            self, cd_id_base64url_encoded: str, cursor=None, limit=100
    ) -> GetConceptDescriptionsResult:
        pass
