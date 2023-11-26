from enum import Enum
from typing import Any, List, Optional, Union, Literal

import rdflib
from pydantic import BaseModel, Field, constr

from app.models.aas_namespace import AASNameSpace
from app.models.rdfiable import RDFiable


class AbstractLangString(BaseModel):
    language: str
    text: constr(min_length=1)

