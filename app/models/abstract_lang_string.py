from enum import Enum
from typing import Any, List, Optional, Union, Literal

from pydantic import BaseModel, Field, constr


class AbstractLangString(BaseModel):
    language: str
    text: constr(min_length=1)
