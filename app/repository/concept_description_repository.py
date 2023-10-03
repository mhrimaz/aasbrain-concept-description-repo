from abc import abstractmethod
from typing import List, Union

from app.models.concept_description import ConceptDescription
from app.models.response import GetConceptDescriptionsResult, Result, RepositoryMetadata


class ConceptDescriptionRepository(object):

    @abstractmethod
    async def connect_to_database(self, db_setting: dict):
        pass

    @abstractmethod
    async def close_database_connection(self):
        pass

    @abstractmethod
    async def get_concept_descriptions(self, query: dict, cursor=None, limit=100) -> Union[GetConceptDescriptionsResult, Result]:
        pass

    @abstractmethod
    async def get_concept_description(self, cd_id_base64url_encoded: str) -> ConceptDescription:
        pass

    @abstractmethod
    async def get_concept_description_history(
        self, cd_id_base64url_encoded: str, cursor=None, limit=100
    ) -> Union[GetConceptDescriptionsResult, Result]:
        pass

    @abstractmethod
    async def get_total_concept_descriptions(self) -> Union[RepositoryMetadata, Result]:
        pass

    @abstractmethod
    async def add_concept_description(self, concept_description: ConceptDescription) -> Union[ConceptDescription,Result]:
        pass

    @abstractmethod
    async def update_concept_description(
        self, cd_id_base64url_encoded: str, concept_description: ConceptDescription
    ) -> Result:
        pass

    @abstractmethod
    async def delete_concept_description(self, cd_id_base64url_encoded: str) -> Result:
        pass

    def get_repository_metadata(self) -> Union[RepositoryMetadata, Result]:
        pass
