from enum import Enum
from typing import Any, List, Optional, Union, Literal

import pydantic
from pydantic import BaseModel, Field, constr

from app.models.blob import Blob
from app.models.file import File
from app.models.multi_language_property import MultiLanguageProperty
from app.models.property import Property
from app.models.range import Range
from app.models.reference_element import ReferenceElement


class SubmodelElementChoice(BaseModel):
    __root__: Union[
        # RelationshipElement,
        # AnnotatedRelationshipElement,
        # BasicEventElement,
        Blob,
        # Capability,
        # Entity,
        File,
        MultiLanguageProperty,
        # Operation,
        Property,
        Range,
        ReferenceElement,
        # SubmodelElementCollection,
        # SubmodelElementList,
    ]
