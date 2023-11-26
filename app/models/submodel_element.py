from enum import Enum
from typing import Any, List, Optional, Union, Literal

import pydantic
from pydantic import BaseModel, Field, constr

from app.models.has_data_specification import HasDataSpecification
from app.models.has_semantics import HasSemantics
from app.models.qualifable import Qualifiable
from app.models.referable import Referable


class SubmodelElement(Referable, HasSemantics, Qualifiable, HasDataSpecification):
    pass
