import json
import os

from app.models.asset_information import AssetInformation
from app.models.concept_description import ConceptDescription
import json

from app.models.property import Property
from app.models.submodel import Submodel
from app.repository.concept_description_repository import base_64_url_encode, base_64_url_decode


def get_testdata_rdf(element: str, type="minimal"):
    content = None
    with open(
        os.path.join(
            os.path.dirname(__file__), "schemas", "schemas", "rdf", "examples", "generated", element, f"{type}.ttl"
        )
    ) as f:
        content = f.read()
    return content


def get_testdata_json(element: str, type="minimal"):
    content = None
    with open(
        os.path.join(
            os.path.dirname(__file__), "schemas", "schemas", "json", "examples", "generated", element, f"{type}.json"
        )
    ) as f:
        content = f.read()
    return content


def test_base64_url():
    value = 'test'
    assert value == base_64_url_decode(base_64_url_encode(value))
    value = "Ä"
    assert value == base_64_url_decode(base_64_url_encode(value))
    value = ""
    assert value == base_64_url_decode(base_64_url_encode(value))


def test_minimal_concept_description():
    concept_description = {
        "id": "something_8ccad77f",
        "modelType": "ConceptDescription",
    }
    cd = ConceptDescription(**concept_description)
    cd_dump = cd.model_dump_json(exclude_none=True)
    assert json.loads(cd_dump) == concept_description


def test_minimal_concept_description_rdf():
    concept_description = {
        "id": "something_8ccad77f",
        "modelType": "ConceptDescription",
    }
    cd = ConceptDescription(**concept_description)
    cd_dump = cd.model_dump_json(exclude_none=True)
    assert json.loads(cd_dump) == concept_description


def test_maximal_concept_description_rdf():
    concept_description = {
        "administration": {"revision": "0", "version": "1230"},
        "category": "something_07a45fb3",
        "description": [
            {
                "language": "Tvwqa-500-8EQd-y-8f5-k-vqdMn7-Ohw9-CcA628-DHKP-hPAjUZ-cnr1REUf-S8-p-9X0r-wtCI-KunG3uzI-7dGUsrTu-fY7-C3-hFN-Y-ML69DgnJ-0-Y0H-TLACBVB-Z0HRibbz-yzSf8dvR-zAn-B-6h8VjcKX-jnwR-0Z8l-ghRIZ7mo-wZG7-zXHdSIV-Oy-8dH00A6L-nJY2dA1-57o8dQ-RpxkBTbE-qBJR-M-DyGDA3U-aguRfIhj-x-XmO-1u",
                "text": "something_863a162e",
            }
        ],
        "displayName": [{"language": "x-Sw4u3ZDO-nJLabnE", "text": "something_c7c0c4c8"}],
        "embeddedDataSpecifications": [
            {
                "dataSpecification": {
                    "keys": [{"type": "Submodel", "value": "urn:example14:c4971d26"}],
                    "type": "ModelReference",
                },
                "dataSpecificationContent": {
                    "modelType": "DataSpecificationIec61360",
                    "preferredName": [
                        {"language": "de-CH", "text": "something_34113ec1"},
                        {"language": "en-UK", "text": "Something random in English 19945c14"},
                    ],
                    "value": "something_a864dcb4",
                },
            }
        ],
        "extensions": [
            {
                "name": "something_aae6caf4",
                "refersTo": [
                    {
                        "keys": [{"type": "Submodel", "value": "urn:another-example01:f7faa581"}],
                        "type": "ModelReference",
                    }
                ],
                "semanticId": {
                    "keys": [{"type": "GlobalReference", "value": "urn:another-company07:4d1bd2cb"}],
                    "type": "ExternalReference",
                },
                "supplementalSemanticIds": [
                    {
                        "keys": [{"type": "GlobalReference", "value": "urn:an-example13:be48ff29"}],
                        "type": "ExternalReference",
                    }
                ],
                "value": "10233",
                "valueType": "xs:unsignedShort",
            }
        ],
        "id": "something_8ccad77f",
        "idShort": "fiZ",
        "isCaseOf": [
            {"keys": [{"type": "GlobalReference", "value": "urn:some-company09:4fffee11"}], "type": "ExternalReference"}
        ],
        "modelType": "ConceptDescription",
    }
    cd = ConceptDescription(**concept_description)
    # for (s,p,o) in cd.to_rdf():
    #     print(s,p,o)
    cd_dump = cd.model_dump_json(exclude_none=True)
    assert json.loads(cd_dump) == concept_description


def test_minimal_asset_information():
    asset_information = {
        "assetKind": "NotApplicable",
        "assetType": "something_9f4c5692",
        "defaultThumbnail": {"path": "file:/M5/%bA:'%9c%6b%ed%00Y*/%4C=4h:d:"},
        "globalAssetId": "something_c71f0c8f",
    }
    pydantic_object = AssetInformation(**asset_information)
    pydantic_object_dump = pydantic_object.model_dump_json(exclude_none=True)
    assert json.loads(pydantic_object_dump) == asset_information


def test_minimal_property():
    payload = {
        "category": "VARIABLE",
        "description": [{"language": "en", "text": "something_be9deae0"}],
        "displayName": [
            {
                "language": "Tvwqa-500-8EQd-y-8f5-k-vqdMn7-Ohw9-CcA628-DHKP-hPAjUZ-cnr1REUf-S8-p-9X0r-wtCI-KunG3uzI-7dGUsrTu-fY7-C3-hFN-Y-ML69DgnJ-0-Y0H-TLACBVB-Z0HRibbz-yzSf8dvR-zAn-B-6h8VjcKX-jnwR-0Z8l-ghRIZ7mo-wZG7-zXHdSIV-Oy-8dH00A6L-nJY2dA1-57o8dQ-RpxkBTbE-qBJR-M-DyGDA3U-aguRfIhj-x-XmO-1u",
                "text": "something_535aeb51",
            }
        ],
        "embeddedDataSpecifications": [
            {
                "dataSpecification": {
                    "keys": [{"type": "Submodel", "value": "urn:another-company15:2bd0986b"}],
                    "type": "ModelReference",
                },
                "dataSpecificationContent": {
                    "modelType": "DataSpecificationIec61360",
                    "preferredName": [
                        {"language": "X-33DQI-g", "text": "something_7e795ee2"},
                        {
                            "language": "en-UK",
                            "text": "Something random in English c8512bdf",
                        },
                    ],
                    "value": "something_4e9c19b7",
                },
            }
        ],
        "extensions": [{"name": "something_aa1af8b3"}],
        "idShort": "PiXO1wyHierj",
        "modelType": "Property",
        "qualifiers": [{"type": "something_500f973e", "valueType": "xs:long"}],
        "semanticId": {
            "keys": [{"type": "GlobalReference", "value": "urn:something00:f4547d0c"}],
            "type": "ExternalReference",
        },
        "supplementalSemanticIds": [
            {
                "keys": [{"type": "Submodel", "value": "urn:another-example10:42487f5a"}],
                "type": "ModelReference",
            }
        ],
        "value": "0061707",
        "valueId": {
            "keys": [{"type": "Submodel", "value": "urn:some-company12:e40857e0"}],
            "type": "ModelReference",
        },
        "valueType": "xs:decimal",
    }
    pydantic_object = Property(**payload)
    pydantic_object_dump = pydantic_object.model_dump_json(exclude_none=True)
    print(pydantic_object_dump)
    print(json.dumps(payload))
    assert json.loads(pydantic_object_dump) == payload


def test_submodel():
    payload = {
        "administration": {},
        "category": "something_91042c92",
        "description": [
            {
                "language": "Tvwqa-500-8EQd-y-8f5-k-vqdMn7-Ohw9-CcA628-DHKP-hPAjUZ-cnr1REUf-S8-p-9X0r-wtCI-KunG3uzI-7dGUsrTu-fY7-C3-hFN-Y-ML69DgnJ-0-Y0H-TLACBVB-Z0HRibbz-yzSf8dvR-zAn-B-6h8VjcKX-jnwR-0Z8l-ghRIZ7mo-wZG7-zXHdSIV-Oy-8dH00A6L-nJY2dA1-57o8dQ-RpxkBTbE-qBJR-M-DyGDA3U-aguRfIhj-x-XmO-1u",
                "text": "something_9a9e9635",
            }
        ],
        "displayName": [{"language": "en", "text": "something_433531c5"}],
        "embeddedDataSpecifications": [
            {
                "dataSpecification": {
                    "keys": [
                        {
                            "type": "GlobalReference",
                            "value": "urn:some-company07:80412e8f",
                        }
                    ],
                    "type": "ExternalReference",
                },
                "dataSpecificationContent": {
                    "modelType": "DataSpecificationIec61360",
                    "preferredName": [
                        {
                            "language": "Tvwqa-500-8EQd-y-8f5-k-vqdMn7-Ohw9-CcA628-DHKP-hPAjUZ-cnr1REUf-S8-p-9X0r-wtCI-KunG3uzI-7dGUsrTu-fY7-C3-hFN-Y-ML69DgnJ-0-Y0H-TLACBVB-Z0HRibbz-yzSf8dvR-zAn-B-6h8VjcKX-jnwR-0Z8l-ghRIZ7mo-wZG7-zXHdSIV-Oy-8dH00A6L-nJY2dA1-57o8dQ-RpxkBTbE-qBJR-M-DyGDA3U-aguRfIhj-x-XmO-1u",
                            "text": "something_be8bb8c1",
                        },
                        {
                            "language": "en-UK",
                            "text": "Something random in English fbebdf98",
                        },
                    ],
                    "value": "something_db2f0b6e",
                },
            }
        ],
        "extensions": [{"name": "something_5b2d373a"}],
        "id": "something_48c66017",
        "idShort": "fiZ",
        "kind": "Instance",
        "modelType": "Submodel",
        "qualifiers": [{"type": "something_031fba58", "valueType": "xs:int"}],
        "semanticId": {
            "keys": [{"type": "GlobalReference", "value": "urn:an-example06:3dc4e5fa"}],
            "type": "ExternalReference",
        },
        "submodelElements": [
            {
                "category": "VARIABLE",
                "description": [{"language": "en", "text": "something_be9deae0"}],
                "displayName": [
                    {
                        "language": "Tvwqa-500-8EQd-y-8f5-k-vqdMn7-Ohw9-CcA628-DHKP-hPAjUZ-cnr1REUf-S8-p-9X0r-wtCI-KunG3uzI-7dGUsrTu-fY7-C3-hFN-Y-ML69DgnJ-0-Y0H-TLACBVB-Z0HRibbz-yzSf8dvR-zAn-B-6h8VjcKX-jnwR-0Z8l-ghRIZ7mo-wZG7-zXHdSIV-Oy-8dH00A6L-nJY2dA1-57o8dQ-RpxkBTbE-qBJR-M-DyGDA3U-aguRfIhj-x-XmO-1u",
                        "text": "something_535aeb51",
                    }
                ],
                "embeddedDataSpecifications": [
                    {
                        "dataSpecification": {
                            "keys": [
                                {
                                    "type": "Submodel",
                                    "value": "urn:another-company15:2bd0986b",
                                }
                            ],
                            "type": "ModelReference",
                        },
                        "dataSpecificationContent": {
                            "modelType": "DataSpecificationIec61360",
                            "preferredName": [
                                {"language": "X-33DQI-g", "text": "something_7e795ee2"},
                                {
                                    "language": "en-UK",
                                    "text": "Something random in English c8512bdf",
                                },
                            ],
                            "value": "something_4e9c19b7",
                        },
                    }
                ],
                "extensions": [{"name": "something_aa1af8b3"}],
                "idShort": "PiXO1wyHierj",
                "modelType": "Property",
                "qualifiers": [{"type": "something_500f973e", "valueType": "xs:long"}],
                "semanticId": {
                    "keys": [{"type": "GlobalReference", "value": "urn:something00:f4547d0c"}],
                    "type": "ExternalReference",
                },
                "supplementalSemanticIds": [
                    {
                        "keys": [
                            {
                                "type": "Submodel",
                                "value": "urn:another-example10:42487f5a",
                            }
                        ],
                        "type": "ModelReference",
                    }
                ],
                "value": "0061707",
                "valueId": {
                    "keys": [{"type": "Submodel", "value": "urn:some-company12:e40857e0"}],
                    "type": "ModelReference",
                },
                "valueType": "xs:decimal",
            }
        ],
    }
    pydantic_object = Submodel(**payload)
    pydantic_object_dump = pydantic_object.model_dump_json(exclude_none=True)
    print(json.dumps(pydantic_object_dump, sort_keys=True))
    print(json.dumps(payload, sort_keys=True))
    assert json.loads(pydantic_object_dump) == payload


def test_maximal_concept_description():
    concept_description = {
        "category": "something_07a45fb3",
        "description": [{"language": "en", "text": "something_863a162e"}],
        "displayName": [{"language": "en", "text": "something_c7c0c4c8"}],
        "embeddedDataSpecifications": [
            {
                "dataSpecification": {
                    "keys": [{"type": "Submodel", "value": "urn:example14:c4971d26"}],
                    "type": "ModelReference",
                },
                "dataSpecificationContent": {
                    "modelType": "DataSpecificationIec61360",
                    "preferredName": [
                        {"language": "de-CH", "text": "something_34113ec1"},
                        {
                            "language": "en-UK",
                            "text": "Something random in English 19945c14",
                        },
                    ],
                    "value": "something_a864dcb4",
                },
            }
        ],
        "extensions": [{"name": "something_4b532e77"}],
        "id": "something_8ccad77f",
        "idShort": "fiZ",
        "isCaseOf": [
            {
                "keys": [{"type": "GlobalReference", "value": "urn:some-company09:4fffee11"}],
                "type": "ExternalReference",
            }
        ],
        "modelType": "ConceptDescription",
    }
    cd = ConceptDescription(**concept_description)
    cd_dump = cd.model_dump_json(exclude_none=True)
    assert json.loads(cd_dump) == concept_description
