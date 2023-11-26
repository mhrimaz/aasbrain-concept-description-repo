from enum import Enum
from typing import Any, List, Optional, Union, Literal

import pydantic
from pydantic import BaseModel, Field, constr


class KeyTypes(Enum):
    AnnotatedRelationshipElement = "AnnotatedRelationshipElement"
    AssetAdministrationShell = "AssetAdministrationShell"
    BasicEventElement = "BasicEventElement"
    Blob = "Blob"
    Capability = "Capability"
    ConceptDescription = "ConceptDescription"
    DataElement = "DataElement"
    Entity = "Entity"
    EventElement = "EventElement"
    File = "File"
    FragmentReference = "FragmentReference"
    GlobalReference = "GlobalReference"
    Identifiable = "Identifiable"
    MultiLanguageProperty = "MultiLanguageProperty"
    Operation = "Operation"
    Property = "Property"
    Range = "Range"
    Referable = "Referable"
    ReferenceElement = "ReferenceElement"
    RelationshipElement = "RelationshipElement"
    Submodel = "Submodel"
    SubmodelElement = "SubmodelElement"
    SubmodelElementCollection = "SubmodelElementCollection"
    SubmodelElementList = "SubmodelElementList"
