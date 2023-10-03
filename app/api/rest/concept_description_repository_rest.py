import json
from typing import Optional

from fastapi import APIRouter
import fastapi
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


@router.get(
    "/concept-descriptions",
    summary="Returns all Concept Descriptions",
    responses={
        200: {
            "model": GetConceptDescriptionsResult,
            "description": "Requested Concept Descriptions",
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
    idShort: Optional[str] = fastapi.Query(
        None, description="The Concept Description’s IdShort"
    ),
    isCaseOf: Optional[str] = fastapi.Query(
        None, description="IsCaseOf reference (UTF8-BASE64-URL-encoded)"
    ),
    dataSpecificationRef: Optional[str] = fastapi.Query(
        None, description="DataSpecification reference (UTF8-BASE64-URL-encoded)"
    ),
    limit: Optional[int] = fastapi.Query(
        100, description="The maximum number of elements in the response array", ge=1
    ),
    cursor: Optional[str] = fastapi.Query(
        None,
        description="A server-generated identifier retrieved from pagingMetadata"
        " that specifies from which position the result listing should continue",
    ),
    cd_repository: ConceptDescriptionRepository = Depends(get_repository),
):
    result = await cd_repository.get_concept_descriptions(
        {}, cursor=cursor, limit=limit
    )
    return JSONResponse(
        json.loads(result.model_dump_json(exclude_none=True)), status_code=200
    )


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
    openapi_extra={
        "x-semanticIds": ["https://admin-shell.io/aas/API/PostConceptDescription/3/0"]
    },
    tags=["Concept Description API"],
)
async def post_concept_description(
    concept_description: ConceptDescription = fastapi.Body(
        ..., description="Concept Description object"
    ),
    cd_repository: ConceptDescriptionRepository = Depends(get_repository),
):
    result = await cd_repository.add_concept_description(concept_description)
    return JSONResponse(
        json.loads(result.model_dump_json(exclude_none=True)), status_code=201
    )


@router.get(
    "/concept-descriptions/{cdIdentifier}",
    summary="Returns a specific Concept Description",
    responses={
        200: {
            "model": ConceptDescription,
            "description": "Requested Concept Description",
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
    openapi_extra={
        "x-semanticIds": [
            "https://admin-shell.io/aas/API/GetConceptDescriptionById/3/0"
        ]
    },
    tags=["Concept Description API"],
)
async def get_concept_description(
    cdIdentifier: str = fastapi.Path(
        ..., description="The Concept Description’s unique id (UTF8-BASE64-URL-encoded)"
    ),
    cd_repository: ConceptDescriptionRepository = Depends(get_repository),
):
    result = await cd_repository.get_concept_description(cdIdentifier)
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
    openapi_extra={
        "x-semanticIds": [
            "https://admin-shell.io/aas/API/PutConceptDescriptionById/3/0"
        ]
    },
    tags=["Concept Description API"],
)
async def update_concept_description(
    cdIdentifier: str = fastapi.Path(
        ..., description="The Concept Description’s unique id (UTF8-BASE64-URL-encoded)"
    ),
    concept_description: ConceptDescription = fastapi.Body(
        ..., description="Concept Description object"
    ),
    cd_repository: ConceptDescriptionRepository = Depends(get_repository),
):
    return {"status": "UP"}


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
    openapi_extra={
        "x-semanticIds": [
            "https://admin-shell.io/aas/API/DeleteConceptDescriptionById/3/0"
        ]
    },
    tags=["Concept Description API"],
)
async def delete_concept_description(
    cdIdentifier: str = fastapi.Path(
        ..., description="The Concept Description’s unique id (UTF8-BASE64-URL-encoded)"
    ),
    cd_repository: ConceptDescriptionRepository = Depends(get_repository),
):
    return {"status": "UP"}


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
    openapi_extra={
        "x-semanticIds": [
            "https://admin-shell.io/aas/API/Descriptor/GetDescription/3/0"
        ]
    },
    tags=["Description API"],
)
async def description():
    return JSONResponse(
        {
            "profiles": [
                "https://admin-shell.io/aas/API/3/0/ConceptDescriptionServiceSpecification/SSP-001"
            ]
        },
        status_code=200,
    )


@router.delete("/concept-descriptions/{cdIdentifier}/history", tags=["Extra"])
async def get_concept_description_history_metadata(
    cd_repository: ConceptDescriptionRepository = Depends(get_repository),
):
    return {"status": "UP"}


@router.delete("/concept-descriptions/{cdIdentifier}/history/{version}", tags=["Extra"])
async def get_concept_description_history(
    cd_repository: ConceptDescriptionRepository = Depends(get_repository),
):
    return {"status": "UP"}


@router.get("/concept-descriptions/metadata", tags=["Extra"])
async def concept_descriptions_metadata():
    return {"status": "UP"}
