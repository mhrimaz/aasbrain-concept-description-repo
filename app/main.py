import json
import logging
from datetime import datetime
from pathlib import Path
from typing import List, Optional
from fastapi.responses import JSONResponse
import uvicorn
from datetime import datetime, timezone
from fastapi import FastAPI
from ariadne import QueryType, make_executable_schema
from ariadne.asgi import GraphQL
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from api.graphql import concept_description_repository_graphql
from api.rest import concept_description_repository_rest
from app.config import get_config
from app.models.response import HealthResponse, Result
from app.repository import get_repository
from fastapi.encoders import jsonable_encoder

app = FastAPI(
    title="Concept Description Repository Service Specification",
    description="The ConceptDescription Repository Service Specification"
                " as part of Details of the Asset Administration Shell metamodel v3",
    version="v3.0.0",
    license_info={
        "name": "MIT License",
        "identifier": "MIT",
    },
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# REST API Endpoints
app.include_router(concept_description_repository_rest.router)

# GraphQL Endpoints
app.mount("/graphql/", GraphQL(concept_description_repository_graphql.schema, debug=True))


@app.get("/health",
         response_model=HealthResponse,
         description="Health checking endpoint",
         tags=["Extra"])
async def check_health() -> HealthResponse:
    return HealthResponse(**{'uptime': 'Unknown'})


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    validation_errors = jsonable_encoder(exc.errors())
    number_of_errors = len(validation_errors)

    error_type = [
        f'[{err.get("type")} -> location: {".".join(map(str, err.get("loc", [""])))}]' for err in validation_errors
    ]
    result = Result(
        **{
            "messages": [
                {
                    "code": "409",
                    "messageType": "Error",
                    "text": f"Invalid payload with {number_of_errors} errors. Reasons {', '.join(error_type)}.",
                    "timestamp": str(datetime.now(timezone.utc).isoformat())
                }
            ]
        }
    )
    return JSONResponse(result.model_dump(), status_code=409)


@app.exception_handler(Exception)
async def exception_handler(request, exc):
    result = Result(
        **{
            "messages": [
                {
                    "code": "500",
                    "messageType": "Error",
                    "text": str(exc),
                    "timestamp": str(datetime.now(timezone.utc).isoformat())
                }
            ]
        }
    )
    return JSONResponse(json.loads(result.model_dump_json()), status_code=500)


async def method_not_allowed(request, exc):
    result = Result(
        **{
            "messages": [
                {
                    "code": "405",
                    "messageType": "Error",
                    "text": f"This method is not allowed on requested endpoint.",
                    "timestamp": str(datetime.now(timezone.utc).isoformat())
                }
            ]
        }
    )
    return JSONResponse(result.model_dump(), status_code=405)


app.add_exception_handler(405, method_not_allowed)
app.add_exception_handler(404, method_not_allowed)


@app.on_event("startup")
async def startup():
    config = get_config()
    # logger.info(f"Startup with Config: {config}")
    repo = await get_repository()
    await repo.connect_to_database({"DB_URI": config.db_uri})


@app.on_event("shutdown")
async def shutdown():
    repo = await get_repository()
    await repo.close_database_connection()


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=9192)
