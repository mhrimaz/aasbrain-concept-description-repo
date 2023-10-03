import json
from typing import Union
from itertools import zip_longest
import redis

from app.models.concept_description import ConceptDescription
from app.models.response import (
    GetConceptDescriptionsResult,
    Result,
    ConceptNotFoundException,
    DuplicateConceptException,
)
from app.repository import ConceptDescriptionRepository
from datetime import datetime, timezone

from app.repository.concept_description_repository import (
    base_64_url_encode,
    base_64_url_decode,
)


class RedisConceptDescriptionRepository(ConceptDescriptionRepository):
    client: redis.Redis = None

    async def connect_to_database(self, db_setting: dict):
        self.client = redis.Redis.from_url(db_setting["DB_URI"])
        self.client.ping()

    async def close_database_connection(self):
        self.client = None

    async def get_concept_descriptions(
        self, query: dict, cursor=None, limit=100
    ) -> GetConceptDescriptionsResult:
        concepts = []
        if cursor is None:
            cursor = 0
        else:
            cursor = int(base_64_url_decode(cursor))
        partial_cursor, partial_keys = self.client.scan(cursor=cursor, count=3)
        for key in partial_keys:
            cd = self.client.get(key)
            concepts.append(json.loads(cd))
        to_return_cursor = ""
        if partial_cursor == 0:
            to_return_cursor = ""
        else:
            to_return_cursor = base_64_url_encode(str(partial_cursor))
        return GetConceptDescriptionsResult(
            **{
                "paging_metadata": {"cursor": to_return_cursor},
                "result": concepts,
            }
        )

    async def get_concept_description(
        self, cd_id_base64url_encoded: str
    ) -> ConceptDescription:
        result = self.client.get(cd_id_base64url_encoded)
        if result is None:
            raise ConceptNotFoundException("Not exist")
        return ConceptDescription.model_validate(json.loads(result))

    async def add_concept_description(
        self, concept_description: ConceptDescription
    ) -> ConceptDescription:
        base64_id = base_64_url_encode(concept_description.id)
        result = self.client.set(
            base64_id, concept_description.model_dump_json(exclude_none=True), nx=True
        )
        if result:
            return concept_description

        raise DuplicateConceptException("Already exists, or another reason")

    async def update_concept_description(
        self, cd_id_base64url_encoded: str, concept_description: ConceptDescription
    ) -> bool:
        pass

    async def delete_concept_description(self, cd_id_base64url_encoded: str) -> bool:
        pass

    async def get_concept_description_history(
        self, cd_id_base64url_encoded: str, cursor=None, limit=100
    ) -> GetConceptDescriptionsResult:
        pass
