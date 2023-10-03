from enum import Enum
from typing import Any, List, Optional, Union, Literal

from pydantic import BaseModel, Field, constr

from app.models.has_data_specification import HasDataSpecification
from app.models.reference import Reference


class AdministrativeInformation(HasDataSpecification):
    version: Optional[constr(min_length=1, max_length=4, pattern=r"^(0|[1-9][0-9]*)$")]
    revision: Optional[constr(min_length=1, max_length=4, pattern=r"^(0|[1-9][0-9]*)$")]
    creator: Optional[Reference] = None
    templateId: Optional[constr(min_length=1, max_length=2000)] = None

