from enum import Enum
from typing import Any, List, Optional, Union, Literal

from pydantic import BaseModel, Field, constr

from app.models.extension import Extension


class HasExtensions(BaseModel):
    extensions: Optional[List[Extension]] = Field(None, min_items=1)
    # TODO: instead of list Set might be better see Constraint AASd-077