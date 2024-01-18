#  MIT License
#
#  Copyright (c) 2023. Mohammad Hossein Rimaz
#
#  Permission is hereby granted, free of charge, to any person obtaining a copy of
#  this software and associated documentation files (the “Software”), to deal in
#  the Software without restriction, including without limitation the rights to use,
#  copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the
#  Software, and to permit persons to whom the Software is furnished to do so, subject
#   to the following conditions:
#
#  The above copyright notice and this permission notice shall be included in all
#  copies or substantial portions of the Software.
#
#  THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED,
#  INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A
#  PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
#  HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF
#  CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE
#  OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

from abc import abstractmethod

from typing import List, Union

from aasbrain_models.concept_description import ConceptDescription
from aasbrain_models.response import GetConceptDescriptionsResult, Result, RepositoryMetadata


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
