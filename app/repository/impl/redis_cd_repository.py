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
    UpdatePayloadIDMismatchException,
)
from app.repository import ConceptDescriptionRepository
from datetime import datetime, timezone

from app.repository.concept_description_repository import (
    base_64_url_encode,
    base_64_url_decode,
)


class RedisConceptDescriptionRepository(ConceptDescriptionRepository):
    client: redis.Redis = None

    async def connect_to_database(self, db_setting: dict, history=True):
        self.client = redis.Redis.from_url(db_setting["DB_URI"])
        self.client.ping()

    async def close_database_connection(self):
        self.client = None

    async def get_concept_descriptions(self, query: dict, cursor=None, limit=100) -> GetConceptDescriptionsResult:
        concepts = []
        if cursor is None:
            cursor = 0
        else:
            cursor = int(base_64_url_decode(cursor))
        partial_cursor, partial_keys = self.client.scan(cursor=cursor, count=limit)
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

    async def get_concept_description(self, cd_id_base64url_encoded: str) -> ConceptDescription:
        result = self.client.get(cd_id_base64url_encoded)
        if result is None:
            raise ConceptNotFoundException("Not exist")
        return ConceptDescription.model_validate(json.loads(result))

    async def add_concept_description(self, concept_description: ConceptDescription) -> ConceptDescription:
        base64_id = base_64_url_encode(concept_description.id)
        # nx flag already checks, it will only works if id does not exist.
        result = self.client.set(base64_id, concept_description.model_dump_json(exclude_none=True), nx=True)
        if result:
            return concept_description

        raise DuplicateConceptException()

    async def update_concept_description(
        self, cd_id_base64url_encoded: str, concept_description: ConceptDescription
    ) -> bool:
        base64_id = base_64_url_encode(concept_description.id)
        # check that the provided id in concept description payload is same
        if base64_id != cd_id_base64url_encoded:
            raise UpdatePayloadIDMismatchException()

        result = self.client.set(base64_id, concept_description.model_dump_json(exclude_none=True), xx=True)
        if result:
            key = cd_id_base64url_encoded + "-history"
            print("DIFF", key)

            return True
        raise ConceptNotFoundException()

    async def delete_concept_description(self, cd_id_base64url_encoded: str) -> bool:
        response = self.client.delete(cd_id_base64url_encoded)
        if response == 0:
            raise ConceptNotFoundException()
        return True

    async def get_concept_description_history(
        self, cd_id_base64url_encoded: str, cursor=None, limit=100
    ) -> GetConceptDescriptionsResult:
        key = cd_id_base64url_encoded + "-history"

        pass
