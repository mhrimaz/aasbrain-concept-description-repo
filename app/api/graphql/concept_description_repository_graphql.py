import json

from ariadne import QueryType, make_executable_schema
from ariadne.asgi import GraphQL
from fastapi import FastAPI
from ariadne import ObjectType, make_executable_schema
from app.models.concept_description import ConceptDescription
from app.models.key import Key, KeyTypes
import os

from app.repository import get_repository
from app.repository.concept_description_repository import base_64_url_encode

type_defs = """
    enum ReferenceTypes{
        ExternalReference
        ModelReference
    }
    
    enum KeyTypes{
        AnnotatedRelationshipElement
        AssetAdministrationShell
        BasicEventElement
        Blob
        Capability
        ConceptDescription
        DataElement
        Entity
        EventElement
        File
        FragmentReference
        GlobalReference
        Identifiable
        MultiLanguageProperty
        Operation
        Property
        Range
        Referable
        ReferenceElement
        RelationshipElement
        Submodel
        SubmodelElement
        SubmodelElementCollection
        SubmodelElementList
    }
    
    enum DataTypeDefXsd{
        xs_anyURI
        xs_base64Binary
        xs_boolean
        xs_byte
        xs_date
        xs_dateTime
        xs_decimal
        xs_double
        xs_duration
        xs_float
        xs_gDay
        xs_gMonth
        xs_gMonthDay
        xs_gYear
        xs_gYearMonth
        xs_hexBinary
        xs_int
        xs_integer
        xs_long
        xs_negativeInteger
        xs_nonNegativeInteger
        xs_nonPositiveInteger
        xs_positiveInteger
        xs_short
        xs_string
        xs_time
        xs_unsignedByte
        xs_unsignedInt
        xs_unsignedLong
        xs_unsignedShort
    }
    
    enum ModelType{
        AnnotatedRelationshipElement
        AssetAdministrationShell
        BasicEventElement
        Blob
        Capability
        ConceptDescription
        DataSpecificationIec61360
        DataElement
        Entity
        File
        MultiLanguageProperty
        Operation
        Property
        Range
        ReferenceElement
        RelationshipElement
        Submodel
        SubmodelElementCollection
        SubmodelElementList
    }
    
    enum DataTypeIec61360{
        BLOB
        BOOLEAN
        DATE
        FILE
        HTML
        INTEGER_COUNT
        INTEGER_CURRENCY
        INTEGER_MEASURE
        IRDI
        IRI
        RATIONAL
        RATIONAL_MEASURE
        REAL_COUNT
        REAL_CURRENCY
        REAL_MEASURE
        STRING
        STRING_TRANSLATABLE
        TIME
        TIMESTAMP
    }
    
    interface AbstractLangString{
        language: String!
        text: String!
    }
    
    type LangStringNameType implements AbstractLangString{
        language: String!
        text: String!
    }
    
    type LangStringTextType implements AbstractLangString{
        language: String!
        text: String!
    }
    
    type Key{
        type: KeyTypes
        value: String!
    }
    
    type Reference{
        type: ReferenceTypes!
        keys: [Key!]!
        referredSemanticId: Reference
    }
    
    interface HasSemantics{
        semanticId: Reference
        supplementalSemanticIds: [Reference!]!
    }
    
    type Extension implements HasSemantics{
        name: String!
        valueType: DataTypeDefXsd
        value: String
        refersTo: [Reference!]!
        semanticId: Reference
        supplementalSemanticIds: [Reference!]!
    }
    
    interface HasExtensions{
        extensions: [Extension!]!
    }
    
    type Referable implements HasExtensions{
        category: String
        idShort: String
        displayName: [LangStringNameType!]
        description: [LangStringTextType!]
        modelType: ModelType!
        extensions: [Extension!]!
    }
    
    type LangStringPreferredNameTypeIec61360 implements AbstractLangString{
        language: String!
        text: String!
    }
    
    type LangStringShortNameTypeIec61360 implements AbstractLangString{
        language: String!
        text: String!
    }
    
    type LangStringDefinitionTypeIec61360 implements AbstractLangString{
        language: String!
        text: String!
    }
    
    type LevelType{
        min: Boolean
        nom: Boolean
        typ: Boolean
        max: Boolean
    }
    
    type ValueReferencePair{
        value: String
        valueId: Reference
    }
    
    type ValueList{
        valueReferencePairs: [ValueReferencePair!]!
    }
    
    type DataSpecificationIec61360{
        preferredName: [LangStringPreferredNameTypeIec61360!]!
        shortName: [LangStringShortNameTypeIec61360!]!
        unit: String
        unitId: String
        dataType: DataTypeIec61360
        definition: [LangStringDefinitionTypeIec61360!]!
        valueFormat: String
        valueList: ValueList
        value: String
        levelType: LevelType
        modelType: ModelType!
    }
    
    type EmbeddedDataSpecification{
        dataSpecification: Reference
        dataSpecificationContent: DataSpecificationIec61360
    }
    
    interface HasDataSpecification{
        embeddedDataSpecifications: [EmbeddedDataSpecification!]
    }
    
    type AdministrativeInformation implements HasDataSpecification{
        version: String
        revision: String
        creator: Reference
        templateId: String
        embeddedDataSpecifications: [EmbeddedDataSpecification!]
    }
    
    interface Identifiable{
        id: String!
        administration: AdministrativeInformation
    }
    
    enum AssetKind{
        Type
        Instance
        NotApplicable
    }
    
    type ConceptDescription implements Identifiable & HasDataSpecification{
        id: String!
        administration: AdministrativeInformation
        embeddedDataSpecifications: [EmbeddedDataSpecification!]
        isCaseOf: [Reference!]
        modelType: ModelType!
    }
    
    type ConceptDescriptionsResult{
        nodes: [ConceptDescription!]
        cursor: String!
    }
    type Query {
        conceptDescriptions(idShort: String, isCaseOf: String, dataSpecificationRef: String, cursor: String, limit: Int): ConceptDescriptionsResult!
        conceptDescription(id: String!): ConceptDescription!
    }
"""


query = QueryType()

concept_descriptions = []

script_dir = os.path.dirname(__file__)
with open(os.path.join(script_dir, "mock_concepts.json")) as mock:
    cds = json.load(mock)
    for cd in cds:
        concept_descriptions.append(ConceptDescription(**cd))
print(concept_descriptions)


@query.field("conceptDescriptions")
def resolve_concept_descriptions(
    _, info, idShort=None, isCaseOf=None, dataSpecificationRef=None, cursor=None, limit=100
):
    cd_list = []
    for cd in concept_descriptions:
        cd_dump = json.loads(cd.model_dump_json(exclude_none=True))
        cd_list.append(cd_dump)
    return {"nodes": cd_list, "cursor": "NotImplemented"}


@query.field("conceptDescription")
async def resolve_concept_description(_, info, id):
    # TODO: this should be efficient
    cd_repository = await get_repository()
    base64_id = base_64_url_encode(id)
    print(await cd_repository.get_concept_description(base64_id))
    cd_list = []
    for cd in concept_descriptions:
        cd_dump = json.loads(cd.model_dump_json(exclude_none=True))
        cd_list.append(cd_dump)
    return cd_list[0]


# Create executable schema instance
schema = make_executable_schema(type_defs, query)
