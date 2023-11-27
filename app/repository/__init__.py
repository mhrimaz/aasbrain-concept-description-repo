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

import asyncio
import json
import os
from base64 import urlsafe_b64encode, urlsafe_b64decode

from app.config import get_config
from app.models.concept_description import ConceptDescription
from app.repository.concept_description_repository import ConceptDescriptionRepository
from app.repository.impl.redis_cd_repository import RedisConceptDescriptionRepository


if get_config().db_backend == "redis":
    cd_repository = RedisConceptDescriptionRepository()
elif get_config().db_backend == "neo4j":
    raise NotImplemented()
elif get_config().db_backend == "mongodb":
    raise NotImplemented()
else:
    raise Exception("Invalid backend provided: redis, neo4j, mongodb")


async def get_repository() -> ConceptDescriptionRepository:
    return cd_repository
