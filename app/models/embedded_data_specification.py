
from enum import Enum
from typing import Any, List, Optional, Union, Literal

from pydantic import BaseModel, Field, constr

from app.models.data_specification_iec_61360 import DataSpecificationIec61360
from app.models.reference import Reference


class EmbeddedDataSpecification(BaseModel):
    dataSpecification: Reference
    dataSpecificationContent: Union[DataSpecificationIec61360]
