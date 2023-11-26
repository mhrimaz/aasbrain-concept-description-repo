from enum import Enum
from typing import Any, List, Optional, Union, Literal

import pydantic
from pydantic import BaseModel, Field, constr


class AssetKind(Enum):
    Instance = "Instance"
    NotApplicable = "NotApplicable"
    Type = "Type"
