from base64 import urlsafe_b64encode, urlsafe_b64decode

from app.config import get_config
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
