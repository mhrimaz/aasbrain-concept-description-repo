#  MIT License
#
#  Copyright (c) 2023. Mohammad Hossein Rimaz
#
#  Permission is hereby granted, free of charge, to any person obtaining a copy of
#  this software and associated documentation files (the “Software”), to deal in
#  the Software without restriction, including without limitation the rights to use,
#  copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the
#  Software, and to permit persons to whom the Software is furnished to do so, subject
#   to the following conditions:
#
#  The above copyright notice and this permission notice shall be included in all
#  copies or substantial portions of the Software.
#
#  THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED,
#  INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A
#  PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
#  HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF
#  CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE
#  OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
from pydantic import BaseModel

from app.models.event_element import EventElement
from app.models.model_type import ModelType
from app.models.reference import Reference
from enum import Enum
from typing import Any, List, Optional, Union, Literal

import pydantic
from pydantic import BaseModel, Field, constr

from app.models.annotated_relationship_element import AnnotatedRelationshipElement
from app.models.blob import Blob
from app.models.file import File
from app.models.multi_language_property import MultiLanguageProperty
from app.models.property import Property
from app.models.range import Range
from app.models.reference_element import ReferenceElement
from app.models.relationship_element import RelationshipElement


class Direction(Enum):
    input = "input"
    output = "output"


class StateOfEvent(Enum):
    off = "off"
    on = "on"


class BasicEventElement(EventElement):
    observed: Reference
    direction: Direction
    state: StateOfEvent
    messageTopic: Optional[
        constr(
            min_length=1,
            max_length=255,
        )
    ] = None
    messageBroker: Optional[Reference] = None
    lastUpdate: Optional[constr()] = None
    minInterval: Optional[constr()] = None
    maxInterval: Optional[constr()] = None
    modelType: Literal["BasicEventElement"] = ModelType.BasicEventElement.value
