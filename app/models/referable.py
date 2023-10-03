from enum import Enum
from typing import Any, List, Optional, Union, Literal

import pydantic
from pydantic import BaseModel, Field, constr

from app.models.has_extensions import HasExtensions
from app.models.lang_string_name_type import LangStringNameType
from app.models.lang_string_text_type import LangStringTextType
from app.models.model_type import ModelType


class Referable(HasExtensions):
    category: Optional[constr(min_length=1, max_length=128, strip_whitespace=True)] = None
    idShort: Optional[constr(min_length=1, max_length=128, pattern=r"^[a-zA-Z][a-zA-Z0-9_]*$")] = None
    displayName: Optional[List[LangStringNameType]] = Field(None, min_items=1)
    description: Optional[List[LangStringTextType]] = Field(None, min_items=1)
    modelType: ModelType
    # TODO: pattern for category and idShort