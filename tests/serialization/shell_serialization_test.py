import json
from typing import List, Any

import rdflib
from pydantic import BaseModel
from rdflib import Graph, RDF

from app.models.aas_namespace import AASNameSpace
from app.models.asset_administraion_shell import AssetAdministrationShell
from app.models.asset_information import AssetInformation
from app.models.concept_description import ConceptDescription
import json

from app.models.data_specification_iec_61360 import DataSpecificationIec61360
from app.models.embedded_data_specification import EmbeddedDataSpecification
from app.models.extension import Extension
from app.models.key import Key
from app.models.property import Property
from app.models.qualifier import Qualifier
from app.models.reference import Reference
from app.models.serializer import TurtleSerializerCustom
from app.models.specific_asset_id import SpecificAssetId
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
    assert re_created == payload


def test_submodel_minimal_to_json():
    payload_json = json.loads(get_testdata_json("Submodel", "minimal"))["submodels"][0]
    payload = Submodel(**payload_json)
    dump = payload.model_dump_json(exclude_none=True)
    assert json.loads(dump) == payload_json


def test_submodel_maximal_to_json():
    payload_json = json.loads(get_testdata_json("Submodel", "maximal"))["submodels"][0]
    payload = Submodel(**payload_json)
    dump = payload.model_dump_json(exclude_none=True)
    assert json.loads(dump) == payload_json


def test_any_submodel_element_maximal_to_json():
    for model in [
        "SubmodelElementList",
        "SubmodelElementCollection",
        "Property",
        "MultiLanguageProperty",
        "Range",
        "Operation",
        "Entity",
        "Capability",
        "Blob",
        "BasicEventElement",
        "AnnotatedRelationshipElement",
        "ReferenceElement",
        "File",
        "RelationshipElement",
    ]:
        payload_json = json.loads(get_testdata_json(model, "maximal"))["submodels"][0]
        payload = Submodel(**payload_json)
        dump = payload.model_dump_json(exclude_none=True)
        assert json.loads(dump) == payload_json


def test_any_submodel_element_minimal_to_json():
    for model in [
        "SubmodelElementList",
        "SubmodelElementCollection",
        "Property",
        "MultiLanguageProperty",
        "Range",
        "Operation",
        "Entity",
        "Capability",
        "Blob",
        "BasicEventElement",
        "AnnotatedRelationshipElement",
        "ReferenceElement",
        "File",
        "RelationshipElement",
    ]:
        payload_json = json.loads(get_testdata_json(model, "minimal"))["submodels"][0]
        payload = Submodel(**payload_json)
        dump = payload.model_dump_json(exclude_none=True)
        assert json.loads(dump) == payload_json


def test_submodel_minimal_to_rdf():
    payload_json = json.loads(get_testdata_json("Submodel", "minimal"))["submodels"][0]
    payload = Submodel(**payload_json)
    graph, created_node = payload.to_rdf()
    print(graph.serialize(format="turtle_custom"))
    re_created = Submodel.from_rdf(graph, created_node)
    assert re_created == payload


def test_submodel_maximal_to_rdf():
    payload_json = json.loads(get_testdata_json("Submodel", "maximal"))["submodels"][0]
    payload = Submodel(**payload_json)
    graph, created_node = payload.to_rdf()
    print(graph.serialize(format="turtle_custom"))
    re_created = Submodel.from_rdf(graph, created_node)
    assert re_created == payload


def test_asset_information_maximal_to_rdf():
    payload_json = json.loads(get_testdata_json("AssetInformation", "maximal"))["assetAdministrationShells"][0]
    payload = AssetAdministrationShell(**payload_json)
    graph, created_node = payload.to_rdf()
    re_created = AssetAdministrationShell.from_rdf(graph, created_node)
    assert re_created == payload


def test_submodel_maximal_to_rdf():
    payload = """
{
    "idShort":"DeviceSpecification",
    "administration":{
        "version":"0",
        "revision":"5"
    },
    "id":"DeviceSpecification",
    "kind":"Instance",
    "qualifiers":[
        {
            "type":"SubmodelTags",
            "valueType":"xs:string",
            "value":"DLCP;DPP"
        }
    ],
    "submodelElements":[
        {
            "category":"CONSTANT",
            "idShort":"DeviceCategory",
            "value":[
                {
                    "category":"CONSTANT",
                    "idShort":"DeviceCategory",
                    "valueType":"xs:string",
                    "value":"Electronic Devices (WEEE)",
                    "modelType":"Property"
                },
                {
                    "category":"CONSTANT",
                    "idShort":"DeviceCategoryDescription",
                    "value":[
                        {
                            "language":"en",
                            "text":"Electrical and electronic waste contains recyclable metals and other materials; recycling them saves resources and protects the environment."
                        }
                    ],
                    "modelType":"MultiLanguageProperty"
                },
                {
                    "category":"CONSTANT",
                    "idShort":"DeviceSubCategory",
                    "valueType":"xs:string",
                    "value":"6",
                    "modelType":"Property"
                },
                {
                    "category":"CONSTANT",
                    "idShort":"DeviceSubcategoryDescription",
                    "value":[
                        {
                            "language":"en",
                            "text":"Small IT Devices"
                        },
                        {
                            "language":"de",
                            "text":"Kleine IT-Ger\u00E4te"
                        }
                    ],
                    "modelType":"MultiLanguageProperty"
                }
            ],
            "modelType":"SubmodelElementCollection"
        },
        {
            "idShort":"DeviceClass",
            "valueType":"xs:string",
            "value":"Digital camera",
            "modelType":"Property"
        },
        {
            "category":"CONSTANT",
            "idShort":"HaveScreen",
            "qualifiers":[
                {
                    "type":"Enum",
                    "valueType":"xs:string",
                    "value":"Yes;No"
                }
            ],
            "valueType":"xs:boolean",
            "value":"0",
            "modelType":"Property"
        },
        {
            "category":"CONSTANT",
            "idShort":"HaveBattery",
            "description":[
                {
                    "language":"de",
                    "text":"Batterien/Akkus enthalten "
                }
            ],
            "qualifiers":[
                {
                    "type":"Enum",
                    "valueType":"xs:string",
                    "value":"Yes;No"
                }
            ],
            "valueType":"xs:boolean",
            "value":"1",
            "modelType":"Property"
        },
        {
            "category":"CONSTANT",
            "idShort":"ExtantChemicalElements",
            "description":[
                {
                    "language":"en",
                    "text":"Chemical system"
                }
            ],
            "modelType":"SubmodelElementCollection"
        },
        {
            "idShort":"DeviceModel",
            "valueType":"xs:string",
            "value":"",
            "modelType":"Property"
        },
        {
            "idShort":"DeviceModelNr",
            "valueType":"xs:string",
            "value":"",
            "modelType":"Property"
        },
        {
            "idShort":"BuildYear",
            "valueType":"xs:date",
            "value":"",
            "modelType":"Property"
        },
        {
            "idShort":"Weight",
            "valueType":"xs:float",
            "value":"50",
            "modelType":"Property"
        },
        {
            "idShort":"BoardSize",
            "description":[
                {
                    "language":"de",
                    "text":"Leiterplattengr\u00F6\u00DFe "
                }
            ],
            "valueType":"xs:float",
            "value":"10",
            "modelType":"Property"
        },
        {
            "idShort":"DeviceAdditionalInfo",
            "valueType":"xs:string",
            "value":"",
            "modelType":"Property"
        }
    ],
    "modelType":"Submodel"
}

    """
    payload_json = json.loads(payload)
    payload = Submodel(**payload_json)
    print(payload)
    graph, created_node = payload.to_rdf()
    print(graph.serialize(format="turtle_custom"))
    re_created = Submodel.from_rdf(graph, created_node)
    assert re_created == payload


def test_any_submodel_element_minimal_to_rdf():
    for model in [
        "Property",
        "MultiLanguageProperty",
        "SubmodelElementCollection",
        "AnnotatedRelationshipElement",
        "File",
        # "Capability",
        # "SubmodelElementList",
        # "Range",
        # "Operation",
        # "Entity",
        # "Blob",
        # "BasicEventElement",
        # "ReferenceElement",
        # "RelationshipElement",
    ]:
        payload_json = json.loads(get_testdata_json(model, "minimal"))["submodels"][0]
        payload = Submodel(**payload_json)
        graph, created_node = payload.to_rdf()
        print(graph.serialize(format="turtle_custom"))
        re_created = Submodel.from_rdf(graph, created_node)
        assert re_created == payload


def test_any_submodel_element_maximal_to_rdf():
    for model in [
        "Property",
        "MultiLanguageProperty",
        "SubmodelElementCollection",
        "AnnotatedRelationshipElement",
        "File",
        # "Capability",
        # "SubmodelElementList",
        # "Range",
        # "Operation",
        # "Entity",
        # "Blob",
        # "BasicEventElement",
        # "ReferenceElement",
        # "RelationshipElement",
    ]:
        payload_json = json.loads(get_testdata_json(model, "maximal"))["submodels"][0]
        payload = Submodel(**payload_json)
        graph, created_node = payload.to_rdf()
        print(graph.serialize(format="turtle_custom"))
        re_created = Submodel.from_rdf(graph, created_node)
        assert re_created == payload


def test_aas_minimal_to_rdf():
    payload_json = json.loads(get_testdata_json("AssetAdministrationShell", "minimal"))["assetAdministrationShells"][0]
    payload = AssetAdministrationShell(**payload_json)
    graph, created_node = payload.to_rdf()
    re_created = AssetAdministrationShell.from_rdf(graph, created_node)
    assert re_created == payload


def test_aas_maximal_to_rdf():
    payload_json = json.loads(get_testdata_json("AssetAdministrationShell", "maximal"))["assetAdministrationShells"][0]
    payload = AssetAdministrationShell(**payload_json)
    graph, created_node = payload.to_rdf()
    re_created = AssetAdministrationShell.from_rdf(graph, created_node)
    assert re_created == payload


def test_asset_information_maximal_to_rdf():
    payload_json = json.loads(get_testdata_json("AssetInformation", "maximal"))["assetAdministrationShells"][0][
        "assetInformation"
    ]
    payload = AssetInformation(**payload_json)
    graph, created_node = payload.to_rdf()
    re_created = AssetInformation.from_rdf(graph, created_node)
    assert re_created == payload


def test_asset_information_to_rdf():
    payload_json = json.loads(get_testdata_json("AssetInformation", "minimal"))["assetAdministrationShells"][0][
        "assetInformation"
    ]
    payload = AssetInformation(**payload_json)
    graph, created_node = payload.to_rdf()
    re_created = AssetInformation.from_rdf(graph, created_node)
    assert re_created == payload


def test_specific_asset_id_maximal_to_rdf():
    payload_json = json.loads(get_testdata_json("SpecificAssetId", "maximal"))["assetAdministrationShells"][0][
        "assetInformation"
    ]["specificAssetIds"][0]
    payload = SpecificAssetId(**payload_json)
    graph, created_node = payload.to_rdf()
    re_created = SpecificAssetId.from_rdf(graph, created_node)
    assert re_created == payload


def test_specific_asset_id_minimal_to_rdf():
    payload_json = json.loads(get_testdata_json("SpecificAssetId", "minimal"))["assetAdministrationShells"][0][
        "assetInformation"
    ]["specificAssetIds"][0]
    payload = SpecificAssetId(**payload_json)
    graph, created_node = payload.to_rdf()
    re_created = SpecificAssetId.from_rdf(graph, created_node)
    assert re_created == payload
