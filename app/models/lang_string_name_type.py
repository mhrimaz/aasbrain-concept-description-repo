from app.models.abstract_lang_string import AbstractLangString

from enum import Enum
from typing import Any, List, Optional, Union, Literal

import pydantic
from pydantic import BaseModel, Field, constr


class LangStringNameType(AbstractLangString):
    text: constr(min_length=1, max_length=128)
