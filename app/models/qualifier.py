from enum import Enum
from typing import Any, List, Optional, Union, Literal

from pydantic import BaseModel, Field, constr

from app.models.data_type_def_xsd import DataTypeDefXsd
from app.models.has_semantics import HasSemantics
from app.models.model_type import ModelType
from app.models.qualifier_kind import QualifierKind
from app.models.reference import Reference


class Qualifier(HasSemantics):
    kind: Optional[QualifierKind] = None
    type: constr(
        min_length=1,
        max_length=128,
    )
    valueType: DataTypeDefXsd
    value: Optional[str] = None
    valueId: Optional[Reference] = None
