from enum import Enum
from typing import Any, List, Optional, Union, Literal

from pydantic import BaseModel, Field, constr

from app.models.data_element import DataElement
from app.models.model_type import ModelType


class File(DataElement):
    value: Optional[str] = None
    contentType: str
    modelType: ModelType = ModelType.File
