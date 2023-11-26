from enum import Enum
from typing import Any, List, Optional, Union, Literal

from pydantic import BaseModel, Field, constr

from app.models.model_type import ModelType
from app.models.qualifier import Qualifier


class Qualifiable(BaseModel):
    qualifiers: Optional[List[Qualifier]] = Field(None, min_items=1)
