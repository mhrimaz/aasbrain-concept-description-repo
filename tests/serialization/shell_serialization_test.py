import json
from typing import List, Any

import rdflib
from pydantic import BaseModel
from rdflib import Graph, RDF
from rdflib.tools.rdf2dot import rdf2dot

from aasbrain_models.aas_namespace import AASNameSpace
from aasbrain_models.asset_administraion_shell import AssetAdministrationShell
from aasbrain_models.asset_information import AssetInformation
from aasbrain_models.concept_description import ConceptDescription
import json

from aasbrain_models.data_specification_iec_61360 import DataSpecificationIec61360
from aasbrain_models.embedded_data_specification import EmbeddedDataSpecification
from aasbrain_models.extension import Extension
from aasbrain_models.key import Key

from aasbrain_models.property import Property
from aasbrain_models.qualifier import Qualifier
from aasbrain_models.reference import Reference
from aasbrain_models.reference_element import ReferenceElement
from aasbrain_models.serializer import TurtleSerializerCustom
from aasbrain_models.specific_asset_id import SpecificAssetId
from aasbrain_models.submodel import Submodel
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


def test_any_submodel_element_to_json():
    elements_in_submodel_env = [
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
    ]
    for test_type in ["minimal", "maximal"]:
        for model in elements_in_submodel_env:
            payload_json = json.loads(get_testdata_json(model, test_type))["submodels"][0]
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


def test_custom_submodel_maximal_to_rdf():
    payload = """
{
    "idShort":"DeviceSubmodel",
    "administration":{
        "version":"0",
        "revision":"5"
    },
    "id":"http://example.com",
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
            "idShort":"DeviceCategorySMC",
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
            "value":[
                 {
                    "idShort":"DeviceModel",
                    "valueType":"xs:string",
                    "value":"",
                    "modelType":"Property"
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
    graph, created_node = payload.to_rdf()
    # print(graph.serialize(format="turtle"))
    graph2, created_node2 = payload.to_rdf(base_uri="https://ns.myaas.ai/dt/")
    # print(graph2.serialize(format="turtle"))
    graph3, created_node3 = payload.to_rdf(base_uri="https://ns.myaas.ai/dt/", id_strategy="base64-url-encode")
    # print(graph3.serialize(format="turtle"))
    graph4, created_node4 = payload.to_rdf(id_strategy="base64-url-encode")
    # print(graph4.serialize(format="turtle"))

    re_created = Submodel.from_rdf(graph, created_node)
    re_created2 = Submodel.from_rdf(graph2, created_node2)
    re_created3 = Submodel.from_rdf(graph3, created_node3)
    re_created4 = Submodel.from_rdf(graph4, created_node4)
    assert re_created == payload
    assert re_created2 == payload
    assert re_created3 == payload
    assert re_created4 == payload



def test_any_submodel_element_to_rdf():
    elements_in_submodel_env = [
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
    ]
    for test_type in ["minimal", "maximal"]:
        for model in elements_in_submodel_env:
            payload_json = json.loads(get_testdata_json(model, test_type))["submodels"][0]
            payload = Submodel(**payload_json)

            graph, created_node = payload.to_rdf()
            re_created = Submodel.from_rdf(graph, created_node)
            assert re_created == payload


def test_aas_minimal_to_rdf():
    payload_json = json.loads(get_testdata_json("AssetAdministrationShell", "minimal"))["assetAdministrationShells"][0]
    payload = AssetAdministrationShell(**payload_json)
    graph, created_node = payload.to_rdf()
    print(graph.serialize(format="turtle_custom"))
    re_created = AssetAdministrationShell.from_rdf(graph, created_node)
    assert re_created == payload


def test_aas_maximal_to_rdf():
    payload_json = json.loads(get_testdata_json("AssetAdministrationShell", "maximal"))["assetAdministrationShells"][0]
    payload = AssetAdministrationShell(**payload_json)
    graph, created_node = payload.to_rdf()
    re_created = AssetAdministrationShell.from_rdf(graph, created_node)
    assert re_created == payload


def test_administrative_information_maximal_to_rdf():
    payload_json = json.loads(get_testdata_json("AdministrativeInformation", "maximal"))["assetAdministrationShells"][0]
    payload = AssetAdministrationShell(**payload_json)
    graph, created_node = payload.to_rdf()
    re_created = AssetAdministrationShell.from_rdf(graph, created_node)
    assert re_created == payload


def test_asset_information_maximal_to_rdf():
    payload_json = json.loads(get_testdata_json("AssetInformation", "maximal"))["assetAdministrationShells"][0][
        "assetInformation"
    ]
    specific_asset_id_payload_json = json.loads(get_testdata_json("SpecificAssetId", "maximal"))[
        "assetAdministrationShells"
    ][0]["assetInformation"]["specificAssetIds"]
    payload_json["specificAssetIds"] = specific_asset_id_payload_json
    payload_json["defaultThumbnail"]["contentType"] = "image/png"
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


def test_entity_with_maximal_specific_asset_id_to_rdf():
    # TODO: fix aas-specs data / validation that specific asset id should be for self-managed
    specific_asset_id_payload_json = json.loads(get_testdata_json("SpecificAssetId", "minimal"))[
        "assetAdministrationShells"
    ][0]["assetInformation"]["specificAssetIds"]
    payload_json = json.loads(get_testdata_json("Entity", "maximal"))["submodels"][0]
    payload_json["submodelElements"][0]["specificAssetIds"] = specific_asset_id_payload_json
    payload = Submodel(**payload_json)
    graph, created_node = payload.to_rdf()
    re_created = Submodel.from_rdf(graph, created_node)
    assert re_created == payload


def test_reference_element_multi_key_to_rdf():
    payload_json = json.loads(
        """
    {
                    "idShort":"someElement",
                    "modelType":"ReferenceElement",
                    "value":{
                        "keys":[
                            {
                                "type":"Submodel",
                                "value":"https://example.com/something"
                            },
                            {
                                "type":"SubmodelElementList",
                                "value":"something_more"
                            },
                            {
                                "type":"Property",
                                "value":"123"
                            }
                        ],
                        "type":"ModelReference"
                    }
                }
                """
    )

    payload_rdf = """
@prefix aas: <https://admin-shell.io/aas/3/0/> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

<changed> a aas:ReferenceElement ;
    
    <https://admin-shell.io/aas/3/0/ReferenceElement/value> [ a aas:Reference ;
            <https://admin-shell.io/aas/3/0/Reference/keys> [ a aas:Key ;
                    <https://admin-shell.io/aas/3/0/Key/type> <https://admin-shell.io/aas/3/0/KeyTypes/SubmodelElementList> ;
                    <https://admin-shell.io/aas/3/0/Key/value> "something_more" ;
                    aas:index 1 ],
                [ a aas:Key ;
                    <https://admin-shell.io/aas/3/0/Key/type> <https://admin-shell.io/aas/3/0/KeyTypes/Property> ;
                    <https://admin-shell.io/aas/3/0/Key/value> "123" ;
                    aas:index 2 ],
                [ a aas:Key ;
                    <https://admin-shell.io/aas/3/0/Key/type> <https://admin-shell.io/aas/3/0/KeyTypes/Submodel> ;
                    <https://admin-shell.io/aas/3/0/Key/value> "https://example.com/something" ;
                    aas:index 0 ] ;
            <https://admin-shell.io/aas/3/0/Reference/type> <https://admin-shell.io/aas/3/0/ReferenceTypes/ModelReference> ] ;

    <https://admin-shell.io/aas/3/0/Referable/idShort> "someElement" .
    """
    payload = ReferenceElement(**payload_json)

    g = rdflib.Graph().parse(data=payload_rdf)
    subject = next(g.subjects(predicate=RDF.type, object=AASNameSpace.AAS["ReferenceElement"]))
    re_created = ReferenceElement.from_rdf(g, subject)
    assert re_created == payload
