#  MIT License
#
#  Copyright (c) 2023. Mohammad Hossein Rimaz
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
from app.models.data_type_def_xsd import DataTypeDefXsd
from app.models.model_type import ModelType
from app.models.reference import Reference
from app.models.specific_asset_id import SpecificAssetId
from app.models.submodel_element import SubmodelElement

from enum import Enum
from typing import Any, List, Optional, Union, Literal

import pydantic
from pydantic import BaseModel, Field, constr


class AasSubmodelElements(Enum):
    AnnotatedRelationshipElement = "AnnotatedRelationshipElement"
    BasicEventElement = "BasicEventElement"
    Blob = "Blob"
    Capability = "Capability"
    DataElement = "DataElement"
    Entity = "Entity"
    EventElement = "EventElement"
    File = "File"
    MultiLanguageProperty = "MultiLanguageProperty"
    Operation = "Operation"
    Property = "Property"
    Range = "Range"
    ReferenceElement = "ReferenceElement"
    RelationshipElement = "RelationshipElement"
    SubmodelElement = "SubmodelElement"
    SubmodelElementCollection = "SubmodelElementCollection"
    SubmodelElementList = "SubmodelElementList"


class SubmodelElementList(SubmodelElement):
    orderRelevant: Optional[bool] = None
    semanticIdListElement: Optional[Reference] = None
    typeValueListElement: AasSubmodelElements
    valueTypeListElement: Optional[DataTypeDefXsd] = None
    value: List["SubmodelElementChoice"] = Field(None, min_length=0, discriminator="modelType")
    modelType: Literal["SubmodelElementList"] = ModelType.SubmodelElementList.value
