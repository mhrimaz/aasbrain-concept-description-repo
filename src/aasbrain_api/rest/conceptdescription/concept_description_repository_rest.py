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
from typing import Optional

import rdflib
from fastapi import APIRouter, Header
import fastapi
from fastapi.openapi.docs import get_redoc_html
from rdflib import Graph

from aasbrain_models.concept_description import ConceptDescription
from aasbrain_models.response import (
    GetConceptDescriptionsResult,
    Result,
    ServiceDescription,
    DatabaseConnectionException,
    ConceptNotFoundException,
    Message,
)
from aasbrain_repository import ConceptDescriptionRepository, get_repository
from fastapi import Depends, FastAPI
from fastapi.responses import JSONResponse

# TODO: Toooo long, refactor and break

router = APIRouter()


@router.get(
    "/concept-descriptions",
    summary="Returns all Concept Descriptions",
    responses={
        200: {
            "description": "Requested Concept Descriptions",
            "model": GetConceptDescriptionsResult,
        },
        400: {
            "model": Result,
            "description": "Bad Request, e.g. the request parameters of the format of the request body is wrong.",
        },
        403: {"model": Result, "description": "Forbidden"},
        500: {"model": Result, "description": "Internal Server Error"},
        "default": {
            "model": Result,
            "description": "Default error handling for unmentioned status codes",
        },
    },
    openapi_extra={
        "x-semanticIds": [
            "https://admin-shell.io/aas/API/GetAllConceptDescriptions/3/0",
            "https://admin-shell.io/aas/API/GetAllConceptDescriptionsByIdShort/3/0",
            "https://admin-shell.io/aas/API/GetAllConceptDescriptionsByIsCaseOf/3/0",
            "https://admin-shell.io/aas/API/GetAllConceptDescriptionsByDataSpecificationReference/3/0",
        ]
    },
    tags=["Concept Description API"],
)
async def get_concept_descriptions(
    idShort: Optional[str] = fastapi.Query(None, description="The Concept Description’s IdShort"),
    isCaseOf: Optional[str] = fastapi.Query(None, description="IsCaseOf reference (UTF8-BASE64-URL-encoded)"),
    dataSpecificationRef: Optional[str] = fastapi.Query(
        None, description="DataSpecification reference (UTF8-BASE64-URL-encoded)"
    ),
    limit: Optional[int] = fastapi.Query(100, description="The maximum number of elements in the response array", ge=1),
    cursor: Optional[str] = fastapi.Query(
        None,
        description="A server-generated identifier retrieved from pagingMetadata"
        " that specifies from which position the result listing should continue",
    ),
    cd_repository: ConceptDescriptionRepository = Depends(get_repository),
):
    result = await cd_repository.get_concept_descriptions(
        query={"idShort": idShort, "isCaseOf": isCaseOf, "dataSpecificationRef": dataSpecificationRef},
        cursor=cursor,
        limit=limit,
    )
    return JSONResponse(json.loads(result.model_dump_json(exclude_none=True)), status_code=200)


@router.post(
    "/concept-descriptions",
    summary="Creates a new Concept Description",
    responses={
        201: {
            "model": ConceptDescription,
            "description": "Concept Description created successfully",
        },
        400: {
            "model": Result,
            "description": "Bad Request, e.g. the request parameters of the format of the request body is wrong.",
        },
        403: {"model": Result, "description": "Forbidden"},
        409: {
            "model": Result,
            "description": "Conflict, a resource which shall be created exists already. Might be thrown if a Submodel or SubmodelElement with the same ShortId is contained in a POST request.",
        },
        500: {"model": Result, "description": "Internal Server Error"},
        "default": {
            "model": Result,
            "description": "Default error handling for unmentioned status codes",
        },
    },
    openapi_extra={"x-semanticIds": ["https://admin-shell.io/aas/API/PostConceptDescription/3/0"]},
    tags=["Concept Description API"],
)
async def post_concept_description(
    concept_description: ConceptDescription = fastapi.Body(
        ..., description="Concept Description object", examples=[{"id": "MyConcept", "modelType": "ConceptDescription"}]
    ),
    cd_repository: ConceptDescriptionRepository = Depends(get_repository),
):
    result = await cd_repository.add_concept_description(concept_description)
    return JSONResponse(json.loads(result.model_dump_json(exclude_none=True)), status_code=201)


@router.get(
    "/concept-descriptions/{cdIdentifier}",
    summary="Returns a specific Concept Description",
    responses={
        200: {
            "model": ConceptDescription,
            "description": "Requested Concept Description",
            "content": {
                "application/json": {"example": ConceptDescription(id="something_8ccad77f")},
                "application/ld+json": {
                    "example": [
                        {
                            "@id": "/something_8ccad77f",
                            "@type": ["https://admin-shell.io/aas/3/0/ConceptDescription"],
                            "https://admin-shell.io/aas/3/0/Identifiable/administration": [
                                {"@value": "something_8ccad77f"}
                            ],
                            "https://admin-shell.io/aas/3/0/Identifiable/id": [{"@value": "something_8ccad77f"}],
                        }
                    ]
                },
                "application/xml": {
                    "example": """<conceptDescription xmlns="https://admin-shell.io/aas/3/0">
    <id>something_8ccad77f</id>
</conceptDescription>
                """,
                    "schema": {"type": "object", "format": "xml", "xml": {"name": "conceptDescription"}},
                },
                "text/turtle": {
                    "example": """@prefix aas: <https://admin-shell.io/aas/3/0/> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix xs: <http://www.w3.org/2001/XMLSchema#> .

<something_8ccad77f> rdf:type aas:ConceptDescription ;
    <https://admin-shell.io/aas/3/0/Identifiable/id> "something_8ccad77f"^^xs:string ;
.
                    """
                },
            },
        },
        400: {
            "model": Result,
            "description": "Bad Request, e.g. the request parameters of the format of the request body is wrong.",
        },
        403: {"model": Result, "description": "Forbidden"},
        404: {"model": Result, "description": "Not Found"},
        500: {"model": Result, "description": "Internal Server Error"},
        "default": {
            "model": Result,
            "description": "Default error handling for unmentioned status codes",
        },
    },
    openapi_extra={"x-semanticIds": ["https://admin-shell.io/aas/API/GetConceptDescriptionById/3/0"]},
    tags=["Concept Description API"],
)
async def get_concept_description(
    request: fastapi.Request,
    cdIdentifier: str = fastapi.Path(..., description="The Concept Description’s unique id (UTF8-BASE64-URL-encoded)"),
    cd_repository: ConceptDescriptionRepository = Depends(get_repository),
):
    content_type = request.headers.get("accept")
    result = await cd_repository.get_concept_description(cdIdentifier)
    if content_type == "application/ld+json":
        g, _ = result.to_rdf()
        return fastapi.Response(
            content=g.serialize(format="json-ld", encoding="utf-8"), media_type="application/ld+json", status_code=200
        )
    if content_type == "text/turtle":
        g, _ = result.to_rdf()
        return fastapi.Response(
            content=g.serialize(format="turtle_custom", encoding="utf-8"), media_type="text/turtle", status_code=200
        )
    if content_type == "application/xml":
        raise NotImplementedError("XML serialization not supported")
    result = result.model_dump_json(exclude_none=True)
    return JSONResponse(json.loads(result), status_code=200)


@router.put(
    "/concept-descriptions/{cdIdentifier}",
    status_code=204,
    summary="Updates an existing Concept Description",
    responses={
        204: {"description": "Concept Description updated successfully"},
        400: {
            "model": Result,
            "description": "Bad Request, e.g. the request parameters of the format of the request body is wrong.",
        },
        403: {"model": Result, "description": "Forbidden"},
        404: {"model": Result, "description": "Not Found"},
        500: {"model": Result, "description": "Internal Server Error"},
        "default": {
            "model": Result,
            "description": "Default error handling for unmentioned status codes",
        },
    },
    openapi_extra={"x-semanticIds": ["https://admin-shell.io/aas/API/PutConceptDescriptionById/3/0"]},
    tags=["Concept Description API"],
)
async def update_concept_description(
    cdIdentifier: str = fastapi.Path(..., description="The Concept Description’s unique id (UTF8-BASE64-URL-encoded)"),
    concept_description: ConceptDescription = fastapi.Body(..., description="Concept Description object"),
    cd_repository: ConceptDescriptionRepository = Depends(get_repository),
):
    return cd_repository.update_concept_description(cdIdentifier, concept_description)


@router.delete(
    "/concept-descriptions/{cdIdentifier}",
    status_code=204,
    summary="Deletes a Concept Description",
    responses={
        204: {"description": "Concept Description deleted successfully"},
        400: {
            "model": Result,
            "description": "Bad Request, e.g. the request parameters of the format of the request body is wrong.",
        },
        403: {"model": Result, "description": "Forbidden"},
        404: {"model": Result, "description": "Not Found"},
        500: {"model": Result, "description": "Internal Server Error"},
        "default": {
            "model": Result,
            "description": "Default error handling for unmentioned status codes",
        },
    },
    openapi_extra={"x-semanticIds": ["https://admin-shell.io/aas/API/DeleteConceptDescriptionById/3/0"]},
    tags=["Concept Description API"],
)
async def delete_concept_description(
    cdIdentifier: str = fastapi.Path(..., description="The Concept Description’s unique id (UTF8-BASE64-URL-encoded)"),
    cd_repository: ConceptDescriptionRepository = Depends(get_repository),
):
    result = await cd_repository.delete_concept_description(cdIdentifier)
    if result:
        return fastapi.Response(status_code=204)

    raise NotImplementedError("TODO: Delete Error exception handling not complete")


@router.get(
    "/description",
    summary="Returns the self-describing information of a network resource (ServiceDescription)",
    responses={
        200: {"model": ServiceDescription, "description": "Requested Description"},
        403: {"model": Result, "description": "Forbidden"},
        "default": {
            "model": Result,
            "description": "Default error handling for unmentioned status codes",
        },
    },
    openapi_extra={"x-semanticIds": ["https://admin-shell.io/aas/API/Descriptor/GetDescription/3/0"]},
    tags=["Description API"],
)
async def description():
    return JSONResponse(
        {"profiles": ["https://admin-shell.io/aas/API/3/0/ConceptDescriptionServiceSpecification/SSP-001"]},
        status_code=200,
    )
