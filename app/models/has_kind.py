from enum import Enum
from typing import Any, List, Optional, Union, Literal

import pydantic
from pydantic import BaseModel, Field, constr

from app.models.has_data_specification import HasDataSpecification
from app.models.identifiable import Identifiable
from app.models.model_type import ModelType
from app.models.modeling_kind import ModellingKind
from app.models.reference import Reference


class HasKind(BaseModel):
    kind: Optional[ModellingKind] = None
