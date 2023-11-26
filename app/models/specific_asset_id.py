from enum import Enum
from typing import Any, List, Optional, Union, Literal

from pydantic import BaseModel, Field, constr

from app.models.has_semantics import HasSemantics
from app.models.reference import Reference


class SpecificAssetId(HasSemantics):
    name: constr(
        min_length=1,
        max_length=64,
    )
    value: constr(
        min_length=1,
        max_length=2000,
    )
    externalSubjectId: Optional[Reference] = None
