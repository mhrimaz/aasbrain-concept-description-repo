from enum import Enum
from typing import Any, List, Optional, Union, Literal

from pydantic import BaseModel, Field, constr

from app.models.abstract_lang_string import AbstractLangString
from app.models.model_type import ModelType
from app.models.reference import Reference


class LangStringPreferredNameTypeIec61360(AbstractLangString):
    text: constr(min_length=1, max_length=255)


class LangStringShortNameTypeIec61360(AbstractLangString):
    text: constr(min_length=1, max_length=18)


class LangStringDefinitionTypeIec61360(AbstractLangString):
    text: constr(min_length=1, max_length=1023)


class DataTypeIec61360(Enum):
    BLOB = 'BLOB'
    BOOLEAN = 'BOOLEAN'
    DATE = 'DATE'
    FILE = 'FILE'
    HTML = 'HTML'
    INTEGER_COUNT = 'INTEGER_COUNT'
    INTEGER_CURRENCY = 'INTEGER_CURRENCY'
    INTEGER_MEASURE = 'INTEGER_MEASURE'
    IRDI = 'IRDI'
    IRI = 'IRI'
    RATIONAL = 'RATIONAL'
    RATIONAL_MEASURE = 'RATIONAL_MEASURE'
    REAL_COUNT = 'REAL_COUNT'
    REAL_CURRENCY = 'REAL_CURRENCY'
    REAL_MEASURE = 'REAL_MEASURE'
    STRING = 'STRING'
    STRING_TRANSLATABLE = 'STRING_TRANSLATABLE'
    TIME = 'TIME'
    TIMESTAMP = 'TIMESTAMP'


class LevelType(BaseModel):
    min: bool
    nom: bool
    typ: bool
    max: bool


class ValueReferencePair(BaseModel):
    value: constr(min_length=1, max_length=2000)
    valueId: Reference


class ValueList(BaseModel):
    valueReferencePairs: List[ValueReferencePair] = Field(..., min_items=1)


class DataSpecificationIec61360(BaseModel):
    preferredName: List[LangStringPreferredNameTypeIec61360] = Field(..., min_items=1)
    shortName: Optional[List[LangStringShortNameTypeIec61360]] = Field(
        None, min_items=1
    )
    unit: Optional[constr(min_length=1)] = None
    unitId: Optional[Reference] = None
    sourceOfDefinition: Optional[constr(min_length=1)] = None
    symbol: Optional[constr(min_length=1)] = None
    dataType: Optional[DataTypeIec61360] = None
    definition: Optional[List[LangStringDefinitionTypeIec61360]] = Field(
        None, min_items=1
    )
    valueFormat: Optional[constr(min_length=1)] = None
    valueList: Optional[ValueList] = None
    value: Optional[constr(min_length=1, max_length=2000)] = None
    levelType: Optional[LevelType] = None
    modelType: ModelType = ModelType.DataSpecificationIec61360
