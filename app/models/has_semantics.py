from enum import Enum
from typing import Any, List, Optional, Union, Literal

from pydantic import BaseModel, Field, constr

from app.models.reference import Reference


class HasSemantics(BaseModel):
    semanticId: Optional[Reference] = None
    supplementalSemanticIds: Optional[List[Reference]] = Field(None, min_items=1)
