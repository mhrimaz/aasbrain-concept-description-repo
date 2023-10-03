from enum import Enum
from typing import Any, List, Optional, Union, Literal

import pydantic
from pydantic import BaseModel, Field, constr

from app.models.administrative_information import AdministrativeInformation
from app.models.referable import Referable


class Identifiable(Referable):
    id: constr(min_length=1, max_length=2000)
    administration: Optional[AdministrativeInformation] = None
