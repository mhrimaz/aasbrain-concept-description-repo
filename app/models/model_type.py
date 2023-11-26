from enum import Enum
from typing import Any, List, Optional, Union, Literal

import pydantic
from pydantic import BaseModel, Field, constr


class ModelType(Enum):
    AnnotatedRelationshipElement = "AnnotatedRelationshipElement"
    AssetAdministrationShell = "AssetAdministrationShell"
    BasicEventElement = "BasicEventElement"
    Blob = "Blob"
    Capability = "Capability"
    ConceptDescription = "ConceptDescription"
    DataSpecificationIec61360 = "DataSpecificationIec61360"
    Entity = "Entity"
    File = "File"
    MultiLanguageProperty = "MultiLanguageProperty"
    Operation = "Operation"
    Property = "Property"
    Range = "Range"
    ReferenceElement = "ReferenceElement"
    RelationshipElement = "RelationshipElement"
    Submodel = "Submodel"
    SubmodelElementCollection = "SubmodelElementCollection"
    SubmodelElementList = "SubmodelElementList"
