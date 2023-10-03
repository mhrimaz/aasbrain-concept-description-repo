
from typing import Any, List, Optional, Union, Literal

import pydantic
from pydantic import BaseModel, Field, constr

from app.models.key import Key
from app.models.reference_types import ReferenceTypes


class Reference(BaseModel):
    type: ReferenceTypes
    keys: List[Key] = Field(..., min_items=1)
    referredSemanticId: 'Reference' = None
