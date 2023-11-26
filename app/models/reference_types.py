from enum import Enum
from typing import Any, List, Optional, Union, Literal

from pydantic import BaseModel, Field, constr


class ReferenceTypes(Enum):
    ExternalReference = "ExternalReference"
    ModelReference = "ModelReference"
