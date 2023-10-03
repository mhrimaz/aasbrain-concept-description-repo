from enum import Enum
from typing import Any, List, Optional, Union, Literal

from pydantic import BaseModel, Field, constr
from app.models.embedded_data_specification import EmbeddedDataSpecification



class HasDataSpecification(BaseModel):

    embeddedDataSpecifications: Optional[List[EmbeddedDataSpecification]] = Field(
        None, min_items=1
    )
