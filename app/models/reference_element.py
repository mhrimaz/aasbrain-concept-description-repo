from enum import Enum
from typing import Any, List, Optional, Union, Literal

from pydantic import BaseModel, Field, constr

from app.models.data_element import DataElement
from app.models.data_type_def_xsd import DataTypeDefXsd
from app.models.lang_string_text_type import LangStringTextType
from app.models.model_type import ModelType
from app.models.reference import Reference


class ReferenceElement(DataElement):
    value: Optional[Reference] = None
    modelType: ModelType = ModelType.ReferenceElement
