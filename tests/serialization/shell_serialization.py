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
from app.models.submodel import Submodel
from tests.model_tests import get_testdata_json, get_testdata_rdf


def test_minimal_asset_information_rdf_to_json():
    payload = get_testdata_rdf("AssetInformation", "maximal")
    g = Graph()
    g.parse(data=payload)
    pred = rdflib.URIRef(AASNameSpace.AAS["AssetAdministrationShell/assetInformation"])
    for o in g.objects(predicate=pred):
        print(g.resource(o))
    assert payload == payload


def test_maximal_asset_information_json_to_rdf():
    payload = get_testdata_json("AssetInformation", "maximal")
    element = AssetInformation(**json.loads(payload)["assetAdministrationShells"][0]["assetInformation"])
    node_graph, new_graph = element.to_rdf()
    assert payload == payload


def test_maximal_asset_information_json_to_rdf():
    payload = get_testdata_json("AssetInformation", "maximal")
    element = AssetInformation(**json.loads(payload)["assetAdministrationShells"][0]["assetInformation"])
    node_graph, new_graph = element.to_rdf()
    for asset_information_subject in new_graph.subjects(predicate=RDF.type, object=AASNameSpace.AAS["AssetInformation"], unique=True):
        asset = AssetInformation.from_rdf(new_graph, asset_information_subject)
    assert payload == payload


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
    payload_json = json.loads(get_testdata_json("Extension", "maximal"))["assetAdministrationShells"][0]["extensions"][0]
    payload = Extension(**payload_json)
    graph, created_node = payload.to_rdf()
    re_created = Extension.from_rdf(graph, created_node)
    assert re_created == payload


def test_extension_minimal_to_rdf():
    payload_json = json.loads(get_testdata_json("Extension", "minimal"))["assetAdministrationShells"][0]["extensions"][0]
    payload = Extension(**payload_json)
    graph, created_node = payload.to_rdf()
    re_created = Extension.from_rdf(graph, created_node)
    assert re_created == payload


def test_data_specification_iec_61360_to_rdf():
    payload_json = json.loads(get_testdata_json("DataSpecificationIec61360", "maximal"))["assetAdministrationShells"][0]["embeddedDataSpecifications"][0]["dataSpecificationContent"]
    payload = DataSpecificationIec61360(**payload_json)
    graph, created_node = payload.to_rdf()
    re_created = DataSpecificationIec61360.from_rdf(graph, created_node)
    assert re_created == payload


def test_embedded_data_specification_to_rdf():
    payload_json = json.loads(get_testdata_json("EmbeddedDataSpecification", "maximal"))["assetAdministrationShells"][0]["embeddedDataSpecifications"][0]
    payload = EmbeddedDataSpecification(**payload_json)
    graph, created_node = payload.to_rdf()
    re_created = EmbeddedDataSpecification.from_rdf(graph, created_node)
    assert re_created == payload


def test_embedded_data_specification_minimal_to_rdf():
    payload_json = json.loads(get_testdata_json("EmbeddedDataSpecification", "minimal"))["assetAdministrationShells"][0]["embeddedDataSpecifications"][0]
    payload = EmbeddedDataSpecification(**payload_json)
    graph, created_node = payload.to_rdf()
    re_created = EmbeddedDataSpecification.from_rdf(graph, created_node)
    assert re_created == payload

def test_concept_description_to_rdf():
    payload_json = json.loads(get_testdata_json("ConceptDescription", "maximal"))["conceptDescriptions"][0]
    payload = ConceptDescription(**payload_json)
    graph, created_node = payload.to_rdf()
    print(Graph.serialize(graph))
    re_created = ConceptDescription.from_rdf(graph, created_node)
    assert re_created == payload


# Example usage
class Address(BaseModel):
    city: str
    street: str


class Person(BaseModel):
    name: str
    age: int
    address: List[Address]


from deepdiff import DeepSearch, grep, DeepDiff, Delta


def test_diff():
    # Create instances
    old_instance = ConceptDescription(id="test",)
    ddiff = DeepDiff(old_instance, new_instance,ignore_order=True,report_repetition=True)
    print(ddiff.to_dict())
    delta = Delta(ddiff)
    print(delta.dumps())
    print(new_instance.model_dump())
    print(old_instance)
    print(old_instance + delta)
    print(new_instance)

