import json
from typing import Optional, List

import rdflib
from fastapi import APIRouter, Header
import fastapi
from fastapi.openapi.docs import get_redoc_html
from rdflib import Graph

from app.models.concept_description import ConceptDescription
from app.models.response import (
    GetConceptDescriptionsResult,
    Result,
    ServiceDescription,
    DatabaseConnectionException,
    ConceptNotFoundException,
)
from app.repository import ConceptDescriptionRepository, get_repository
from fastapi import Depends, FastAPI
from fastapi.responses import JSONResponse

router = APIRouter()


@router.get("/concept-descriptions/{cdIdentifier}/history", tags=["Extra"])
async def get_concept_description_history_metadata(
    cd_repository: ConceptDescriptionRepository = Depends(get_repository),
):
    raise NotImplementedError("History endpoint not implemented.")


@router.get("/concept-descriptions/{cdIdentifier}/history/{version}", tags=["Extra"])
async def get_concept_description_history(
    cd_repository: ConceptDescriptionRepository = Depends(get_repository),
):
    raise NotImplementedError("History endpoint not implemented.")


@router.get("/concept-descriptions/metadata", tags=["Extra"])
async def concept_descriptions_metadata():
    raise NotImplementedError("Metadata endpoint not implemented.")


# Follows google api guideline
# https://cloud.google.com/apis/design/custom_methods


@router.post("/concept-descriptions:search", tags=["Extra"])
async def search_concept_descriptions(
    concepts: List[ConceptDescription],
    cd_repository: ConceptDescriptionRepository = Depends(get_repository),
):
    raise NotImplementedError("History metadata endpoint not implemented.")


@router.post("/concept-descriptions:bulkCreate", tags=["Extra"])
async def atomic_bulk_create_concept_descriptions(
    concepts: List[ConceptDescription],
    cd_repository: ConceptDescriptionRepository = Depends(get_repository),
):
    raise NotImplementedError("History metadata endpoint not implemented.")


@router.post("/concept-descriptions:bulkDelete", tags=["Extra"])
async def atomic_bulk_delete_concept_descriptions(
    concepts_id: List[str],
    cd_repository: ConceptDescriptionRepository = Depends(get_repository),
):
    raise NotImplementedError("History metadata endpoint not implemented.")


@router.post("/concept-descriptions:bulkUpdate", tags=["Extra"])
async def atomic_bulk_update_concept_descriptions(
    concepts: List[ConceptDescription],
    cd_repository: ConceptDescriptionRepository = Depends(get_repository),
):
    raise NotImplementedError("History metadata endpoint not implemented.")
