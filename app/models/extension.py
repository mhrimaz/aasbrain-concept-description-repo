from enum import Enum
from typing import Any, List, Optional, Union, Literal

from pydantic import BaseModel, Field, constr

from app.models.data_type_def_xsd import DataTypeDefXsd
from app.models.has_semantics import HasSemantics
from app.models.reference import Reference


class Extension(HasSemantics):
    name: constr(min_length=1, max_length=128)
    valueType: Optional[DataTypeDefXsd] = None
    value: Optional[str] = None
    refersTo: Optional[List[Reference]] = Field(None, min_items=1)