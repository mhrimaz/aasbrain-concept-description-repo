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
import os
from contextlib import asynccontextmanager
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.responses import JSONResponse
import uvicorn
from datetime import datetime, timezone
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from loguru import logger
from starlette.responses import RedirectResponse
from starlette.staticfiles import StaticFiles

from aasbrain_api.graphql import concept_description_repository_graphql
from aasbrain_api.rest.conceptdescription import (
    concept_description_repository_rest,
    concept_description_repository_extra_rest,
)
from aasbrain_api.rest import rdf_utility_rest
from .config import get_config
from aasbrain_models.concept_description import ConceptDescription
from aasbrain_models.response import HealthResponse, Result, MessageType, APIException
from aasbrain_repository import get_repository
from fastapi.encoders import jsonable_encoder


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    config = get_config()
    logger.info(f"Startup with Config: {config}")
    repo = await get_repository()
    await repo.connect_to_database({"DB_URI": config.db_uri})
    script_dir = os.path.dirname(__file__)
    with open(os.path.join(script_dir, "repository", "mock_concepts.json"), encoding="utf-8") as mock:
        cds = json.load(mock)
        cd_repo = await get_repository()
        for cd in cds:
            try:
                await cd_repo.add_concept_description(ConceptDescription(**cd))
            except:
                pass

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

# Include Official Concept Description REST API Endpoints
app.include_router(concept_description_repository_rest.router)

# Include RDF Utility
app.include_router(rdf_utility_rest.router)

# Include Extra Features
app.include_router(concept_description_repository_extra_rest.router)

# Include Concept Description GraphQL Endpoints
app.mount(
    "/graphql/",
    concept_description_repository_graphql.router,
    name="GraphQL",
)


@app.get("/health", response_model=HealthResponse, description="Health checking endpoint", tags=["Extra"])
async def check_health() -> HealthResponse:
    return HealthResponse(**{"status": "Obviously UP!", "uptime": "Who knows?!"})


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
    if isinstance(exc, APIException):
        result = Result(
            **{
                "messages": [
                    {
                        "code": str(exc.error_code),
                        "messageType": "Error",
                        "text": str(exc.message),
                        "timestamp": str(datetime.now(timezone.utc).isoformat()),
                    }
                ]
            }
        )
    else:
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
    # Serve the frontend (Vue.js) as static files
    app.mount("/home/", StaticFiles(directory="ui/cd-ui/dist", html=True), name="static")

    @app.get("/", include_in_schema=False)
    async def home():
        return RedirectResponse(url="/home/")

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
