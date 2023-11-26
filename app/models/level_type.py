from enum import Enum
from typing import Any, List, Optional, Union, Literal

from pydantic import BaseModel, Field, constr


class LevelType(BaseModel):
    min: bool
    nom: bool
    typ: bool
    max: bool
