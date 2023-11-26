import json
from typing import List, Any

import rdflib
from pydantic import BaseModel
from rdflib import Graph, RDF

from app.models.aas_namespace import AASNameSpace
from app.models.asset_information import AssetInformation
from app.models.concept_description import ConceptDescription
import json

from app.models.data_specification_iec_61360 import DataSpecificationIec61360
from app.models.embedded_data_specification import EmbeddedDataSpecification
from app.models.extension import Extension
from app.models.key import Key
from app.models.property import Property
from app.models.reference import Reference
from app.models.serializer import TurtleSerializerCustom
from app.models.submodel import Submodel
from tests.model_test import get_testdata_json, get_testdata_rdf


def test_key_to_rdf():
    payload = Key(**{"type": "AssetAdministrationShell", "value": "example"})
    graph, created_node = payload.to_rdf()
    re_created = Key.from_rdf(graph, created_node)
    assert re_created == payload


def test_reference_to_rdf():
    payload_json = json.loads(get_testdata_json("Reference", "maximal"))["assetAdministrationShells"][0]["derivedFrom"]
    payload = Reference(**payload_json)
    graph, created_node = payload.to_rdf()
    re_created = Reference.from_rdf(graph, created_node)
    assert re_created == payload


def test_extension_to_rdf():
    payload_json = json.loads(get_testdata_json("Extension", "maximal"))["assetAdministrationShells"][0]["extensions"][
        0
    ]
    payload = Extension(**payload_json)
    graph, created_node = payload.to_rdf()
    re_created = Extension.from_rdf(graph, created_node)
    assert re_created == payload


def test_extension_minimal_to_rdf():
    payload_json = json.loads(get_testdata_json("Extension", "minimal"))["assetAdministrationShells"][0]["extensions"][
        0
    ]
    payload = Extension(**payload_json)
    graph, created_node = payload.to_rdf()
    re_created = Extension.from_rdf(graph, created_node)
    assert re_created == payload


def test_data_specification_iec_61360_to_rdf():
    payload_json = json.loads(get_testdata_json("DataSpecificationIec61360", "maximal"))["assetAdministrationShells"][
        0
    ]["embeddedDataSpecifications"][0]["dataSpecificationContent"]
    payload = DataSpecificationIec61360(**payload_json)
    graph, created_node = payload.to_rdf()
    re_created = DataSpecificationIec61360.from_rdf(graph, created_node)
    assert re_created == payload


def test_embedded_data_specification_to_rdf():
    payload_json = json.loads(get_testdata_json("EmbeddedDataSpecification", "maximal"))["assetAdministrationShells"][
        0
    ]["embeddedDataSpecifications"][0]
    payload = EmbeddedDataSpecification(**payload_json)
    graph, created_node = payload.to_rdf()
    re_created = EmbeddedDataSpecification.from_rdf(graph, created_node)
    assert re_created == payload


def test_embedded_data_specification_minimal_to_rdf():
    payload_json = json.loads(get_testdata_json("EmbeddedDataSpecification", "minimal"))["assetAdministrationShells"][
        0
    ]["embeddedDataSpecifications"][0]
    payload = EmbeddedDataSpecification(**payload_json)
    graph, created_node = payload.to_rdf()
    re_created = EmbeddedDataSpecification.from_rdf(graph, created_node)
    assert re_created == payload


def test_concept_description_to_rdf():
    payload_json = json.loads(get_testdata_json("ConceptDescription", "maximal"))["conceptDescriptions"][0]
    payload = ConceptDescription(**payload_json)
    graph, created_node = payload.to_rdf()
    re_created = ConceptDescription.from_rdf(graph, created_node)
    g2 = Graph().parse(data=graph.serialize())
    assert re_created == payload