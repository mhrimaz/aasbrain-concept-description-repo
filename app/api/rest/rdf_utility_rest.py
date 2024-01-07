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

import json
from typing import Optional, List

import rdflib
from fastapi import APIRouter, Header
import fastapi
from fastapi.openapi.docs import get_redoc_html
from rdflib import Graph

from app.models.aas_namespace import AASNameSpace
from app.models.asset_administraion_shell import AssetAdministrationShell
from app.models.concept_description import ConceptDescription
from app.models.response import (
    GetConceptDescriptionsResult,
    Result,
    ServiceDescription,
    DatabaseConnectionException,
    ConceptNotFoundException,
)
from app.models.submodel import Submodel
from app.repository import ConceptDescriptionRepository, get_repository
from fastapi import Depends, FastAPI
from fastapi.responses import JSONResponse

router = APIRouter()


@router.post("/submodel:jsontordf", tags=["RDF"])
async def convert_submodel_to_rdf(
    submodel=fastapi.Body(..., examples=[{"id": "MySubmodel", "modelType": "Submodel"}]),
):
    payload = Submodel(**submodel)
    graph, _ = payload.to_rdf()
    return fastapi.Response(
        content=graph.serialize(format="turtle_custom", encoding="utf-8"), media_type="text/turtle", status_code=200
    )


@router.post("/submodel:rdftojson", tags=["RDF"])
async def convert_submodel_to_json(
    submodel: str = fastapi.Body(
        ...,
        media_type="text/turtle",
        examples=[
            '@prefix aas: <https://admin-shell.io/aas/3/0/> . \n\n[] a aas:Submodel ;\n    <https://admin-shell.io/aas/3/0/Identifiable/id> "MySubmodel" .'
        ],
    ),
):
    graph = rdflib.Graph().parse(data=submodel, format="turtle")
    # Only consider the instance of ConceptDescription.
    target: rdflib.URIRef = next(graph.subjects(predicate=rdflib.Graph, object=AASNameSpace.AAS["Submodel"]), None)
    payload = Submodel.from_rdf(graph, target)
    result = payload.model_dump_json(exclude_none=True)
    return JSONResponse(json.loads(result), status_code=200)


@router.post("/concept-description:jsontordf", tags=["RDF"])
async def convert_concept_description_to_rdf(
    concept=fastapi.Body(..., examples=[{"id": "MyConcept", "modelType": "ConceptDescription"}]),
):
    payload = ConceptDescription(**concept)
    graph, _ = payload.to_rdf()
    return fastapi.Response(
        content=graph.serialize(format="turtle_custom", encoding="utf-8"), media_type="text/turtle", status_code=200
    )


@router.post("/concept-description:rdftojson", tags=["RDF"])
async def convert_concept_description_to_json(
    concept: str = fastapi.Body(
        ...,
        media_type="text/turtle",
        examples=[
            '@prefix aas: <https://admin-shell.io/aas/3/0/> . \n\n<TXlDb25jZXB0> a aas:ConceptDescription ; \n    <https://admin-shell.io/aas/3/0/Identifiable/id> "MyConcept" .'
        ],
    ),
):
    graph = rdflib.Graph().parse(data=concept, format="turtle")
    print(graph.serialize(format="turtle"))
    # Only consider the instance of ConceptDescription.
    target: rdflib.URIRef = next(
        graph.subjects(predicate=rdflib.Graph, object=AASNameSpace.AAS["ConceptDescription"]), None
    )
    payload = ConceptDescription.from_rdf(graph, target)
    result = payload.model_dump_json(exclude_none=True)
    return JSONResponse(json.loads(result), status_code=200)


@router.post("/shell:jsontordf", tags=["RDF"])
async def convert_shell_to_rdf(
    shell=fastapi.Body(
        ...,
        examples=[
            {"id": "MyShell", "assetInformation": {"assetKind": "Instance"}, "modelType": "AssetAdministrationShell"}
        ],
    ),
):
    payload = AssetAdministrationShell(**shell)
    graph, _ = payload.to_rdf()
    return fastapi.Response(
        content=graph.serialize(format="turtle_custom", encoding="utf-8"), media_type="text/turtle", status_code=200
    )


@router.post("/shell:rdftojson", tags=["RDF"])
async def convert_shell_to_json(
    shell: str = fastapi.Body(
        ...,
        media_type="text/turtle",
        examples=[
            '@prefix aas: <https://admin-shell.io/aas/3/0/> . \n\n<https://example.com/shell/1> a aas:AssetAdministrationShell ;\n    <https://admin-shell.io/aas/3/0/Identifiable/id> "MyShell";\n    <https://admin-shell.io/aas/3/0/AssetAdministrationShell/assetInformation> [ a aas:AssetInformation ;\n        <https://admin-shell.io/aas/3/0/AssetInformation/assetKind> <https://admin-shell.io/aas/3/0/AssetKind/Instance> ] .'
        ],
    ),
):
    graph = rdflib.Graph().parse(data=shell, format="turtle")
    # Only consider the instance of ConceptDescription.
    target: rdflib.URIRef = next(
        graph.subjects(predicate=rdflib.Graph, object=AASNameSpace.AAS["AssetAdministrationShell"]), None
    )
    payload = AssetAdministrationShell.from_rdf(graph, target)
    result = payload.model_dump_json(exclude_none=True)
    return JSONResponse(json.loads(result), status_code=200)
