import json
import logging
from contextlib import asynccontextmanager
from datetime import datetime
from pathlib import Path
from typing import List, Optional

import fastapi
from ariadne.explorer import ExplorerGraphiQL
from fastapi.openapi.docs import get_redoc_html, get_swagger_ui_html
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
from app.api.rest import concept_description_repository_extra_rest
from app.config import get_config
from app.models.response import HealthResponse, Result, MessageType
from app.repository import get_repository
from fastapi.encoders import jsonable_encoder


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    config = get_config()
    # logger.info(f"Startup with Config: {config}")
    repo = await get_repository()
    await repo.connect_to_database({"DB_URI": config.db_uri})

    yield
    # Shutdown
    repo = await get_repository()
    await repo.close_database_connection()


app = FastAPI(
    title="AAS Brain Concept Description Repository",
    description="The ConceptDescription Repository Service Specification"
    " as part of Details of the Asset Administration Shell metamodel V3",
    version="v3.0.0",
    license_info={
        "name": "MIT License",
        "identifier": "MIT",
    },
    contact={
        "name": "Mohammad Hossein Rimaz",
        "url": "https://www.linkedin.com/in/mhrimaz/",
        "email": "mrimaz@acm.org",
    },
    redoc_url=None,
    docs_url=None,
    lifespan=lifespan,
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

# Include Extra Features
app.include_router(concept_description_repository_extra_rest.router)

# GraphQL Endpoints
default_graphql_query = """# AAS Brain Concept Description GraphQL Endpoint
# GraphiQL is an in -browser tool for writing, validating, and
# testing GraphQL queries.
#
# Type queries into this side of the screen, and you will see intelligent
# typeaheads aware of the current GraphQL type schema and live syntax and
# validation errors highlighted within the text.
#
# GraphQL queries typically start with a "{" character. Lines that start
# with a # are ignored.
#
# An example GraphQL query might look like:
#
{
  conceptDescription(id:"MyConcept"){
    id
#    embeddedDataSpecifications{
#      dataSpecificationContent{
#        unit
#        preferredName{
#          text
#       }
#      }
#    }
  }
}
#
# Keyboard shortcuts:
#   Prettify query: Shift - Ctrl - P(or press the prettify button)
#   Run Query: Ctrl - Enter(or press the play button)
#   Auto Complete: Ctrl - Space(or just start typing)
#   Merge fragments: Shift - Ctrl - M(or press the merge button)"""
app.mount(
    "/graphql/",
    GraphQL(
        concept_description_repository_graphql.schema,
        debug=True,
        explorer=ExplorerGraphiQL(title="AAS Brain GraphQL", default_query=default_graphql_query),
    ),
    name="GraphQL",
)


@app.get("/health", response_model=HealthResponse, description="Health checking endpoint", tags=["Extra"])
async def check_health() -> HealthResponse:
    return HealthResponse(**{"status":"Obviously UP!","uptime": "Who knows?!"})


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
                    "timestamp": str(datetime.now(timezone.utc).isoformat()),
                }
            ]
        }
    )
    return JSONResponse(result.model_dump(), status_code=409)


@app.exception_handler(Exception)
async def exception_handler(request, exc):
    # TODO: change code and messageType based on exception
    result = Result(
        **{
            "messages": [
                {
                    "code": "500",
                    "messageType": "Error",
                    "text": str(exc),
                    "timestamp": str(datetime.now(timezone.utc).isoformat()),
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
                    "messageType": MessageType.Exception,
                    "text": f"This method is not allowed on requested endpoint.",
                    "timestamp": str(datetime.now(timezone.utc).isoformat()),
                }
            ]
        }
    )
    return JSONResponse(result.model_dump_json(exclude_none=True), status_code=405)


app.add_exception_handler(405, method_not_allowed)
app.add_exception_handler(404, method_not_allowed)


@app.get("/docs", include_in_schema=False)
def swagger_html():
    return get_swagger_ui_html(openapi_url="/openapi.json", title="AAS Brain", swagger_favicon_url="")


@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    # TODO: add favicon
    return None


include_ui = False
if include_ui:

    @app.get("/", include_in_schema=False)
    async def home():
        # TODO: add ui
        return "No UI!"

else:

    @app.get("/", include_in_schema=False)
    def home_as_swagger_ui():
        return swagger_html()


# @app.get("/redoc", include_in_schema=True)
# async def redoc_html():
#     return get_redoc_html(
#         openapi_url="/openapi.json",
#         title=app.title + " - ReDoc",
#         redoc_js_url="https://cdn.jsdelivr.net/npm/redoc/bundles/redoc.standalone.js",
#     )

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=9192)
