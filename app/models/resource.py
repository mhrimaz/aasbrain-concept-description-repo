from enum import Enum
from typing import Any, List, Optional, Union, Literal

from pydantic import BaseModel, Field, constr


# TODO: recheck
class Resource(BaseModel):
    path: str
    contentType: Optional[str] = None
