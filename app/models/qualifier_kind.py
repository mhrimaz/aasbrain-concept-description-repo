from enum import Enum
from typing import Any, List, Optional, Union, Literal

from pydantic import BaseModel, Field, constr

from app.models.has_semantics import HasSemantics
from app.models.model_type import ModelType


class QualifierKind(Enum):
    ConceptQualifier = "ConceptQualifier"
    TemplateQualifier = "TemplateQualifier"
    ValueQualifier = "ValueQualifier"
