import json

from app.models.concept_description import ConceptDescription
import json


def test_minimal_concept_description():
    concept_description = {
        "id": "something_8ccad77f",
        "modelType": "ConceptDescription"
    }
    cd = ConceptDescription(**concept_description)
    cd_dump = cd.model_dump_json(exclude_none=True)
    assert json.loads(cd_dump) == concept_description


def test_maximal_concept_description():
    concept_description = {
        "category": "something_07a45fb3",
        "description": [
            {
                "language": "en",
                "text": "something_863a162e"
            }
        ],
        "displayName": [
            {
                "language": "en",
                "text": "something_c7c0c4c8"
            }
        ],
        "embeddedDataSpecifications": [
            {
                "dataSpecification": {
                    "keys": [
                        {
                            "type": "Submodel",
                            "value": "urn:example14:c4971d26"
                        }
                    ],
                    "type": "ModelReference"
                },
                "dataSpecificationContent": {
                    "modelType": "DataSpecificationIec61360",
                    "preferredName": [
                        {
                            "language": "de-CH",
                            "text": "something_34113ec1"
                        },
                        {
                            "language": "en-UK",
                            "text": "Something random in English 19945c14"
                        }
                    ],
                    "value": "something_a864dcb4"
                }
            }
        ],
        "extensions": [
            {
                "name": "something_4b532e77"
            }
        ],
        "id": "something_8ccad77f",
        "idShort": "fiZ",
        "isCaseOf": [
            {
                "keys": [
                    {
                        "type": "GlobalReference",
                        "value": "urn:some-company09:4fffee11"
                    }
                ],
                "type": "ExternalReference"
            }
        ],
        "modelType": "ConceptDescription"
    }
    cd = ConceptDescription(**concept_description)
    cd_dump = cd.model_dump_json(exclude_none=True)
    assert json.loads(cd_dump) == concept_description
