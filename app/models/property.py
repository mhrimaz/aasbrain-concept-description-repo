from enum import Enum
from typing import Any, List, Optional, Union, Literal

from pydantic import BaseModel, Field, constr

from app.models.data_element import DataElement

from enum import Enum
from typing import Any, List, Optional, Union, Literal

from pydantic import BaseModel, Field, constr

from app.models.data_type_def_xsd import DataTypeDefXsd
from app.models.model_type import ModelType
from app.models.reference import Reference


class Property(DataElement):
    valueType: DataTypeDefXsd
    value: Optional[str] = None
    valueId: Optional[Reference] = None
    modelType: Literal["Property"]
