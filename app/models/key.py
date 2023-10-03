from enum import Enum
from typing import Any, List, Optional, Union, Literal

import pydantic
from pydantic import BaseModel, Field, constr

from app.models.key_types import KeyTypes


class Key(BaseModel):
    type: KeyTypes
    value: constr(min_length=1, max_length=2000)
    # TODO: Add Pattern for Key