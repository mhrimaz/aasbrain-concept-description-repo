#  MIT License
#
#  Copyright (c) 2024. Mohammad Hossein Rimaz
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

#  MIT License
#
#
#  Permission is hereby granted, free of charge, to any person obtaining a copy of
#  this software and associated documentation files (the “Software”), to deal in
#  the Software without restriction, including without limitation the rights to use,
#  copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the
#  Software, and to permit persons to whom the Software is furnished to do so, subject
#   to the following conditions:
#
#
import json
from typing import Optional, List

import rdflib
from fastapi import APIRouter, Header
import fastapi
from fastapi.openapi.docs import get_redoc_html
from rdflib import Graph

from aasbrain_models.aas_namespace import AASNameSpace
from aasbrain_models.asset_administraion_shell import AssetAdministrationShell
from aasbrain_models.concept_description import ConceptDescription
from aasbrain_models.response import (
    GetConceptDescriptionsResult,
    Result,
    ServiceDescription,
    DatabaseConnectionException,
    ConceptNotFoundException,
)
from aasbrain_models.submodel import Submodel
from aasbrain_repository import ConceptDescriptionRepository, get_repository
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
    raise NotImplementedError("Search endpoint not implemented.")


@router.post("/concept-descriptions:bulkCreate", tags=["Extra"])
async def atomic_bulk_create_concept_descriptions(
    concepts: List[ConceptDescription],
    cd_repository: ConceptDescriptionRepository = Depends(get_repository),
):
    raise NotImplementedError("Bulk create endpoint not implemented.")


@router.post("/concept-descriptions:bulkDelete", tags=["Extra"])
async def atomic_bulk_delete_concept_descriptions(
    concepts_id: List[str],
    cd_repository: ConceptDescriptionRepository = Depends(get_repository),
):
    raise NotImplementedError("Bulk delete endpoint not implemented.")


@router.post("/concept-descriptions:bulkUpdate", tags=["Extra"])
async def atomic_bulk_update_concept_descriptions(
    concepts: List[ConceptDescription],
    cd_repository: ConceptDescriptionRepository = Depends(get_repository),
):
    raise NotImplementedError("Bulk update endpoint not implemented.")
