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

from enum import Enum
from typing import Any, List, Optional, Union, Literal

from pydantic import BaseModel, Field, constr


class DataTypeDefXsd(Enum):
    xs_anyURI = "xs:anyURI"
    xs_base64Binary = "xs:base64Binary"
    xs_boolean = "xs:boolean"
    xs_byte = "xs:byte"
    xs_date = "xs:date"
    xs_dateTime = "xs:dateTime"
    xs_decimal = "xs:decimal"
    xs_double = "xs:double"
    xs_duration = "xs:duration"
    xs_float = "xs:float"
    xs_gDay = "xs:gDay"
    xs_gMonth = "xs:gMonth"
    xs_gMonthDay = "xs:gMonthDay"
    xs_gYear = "xs:gYear"
    xs_gYearMonth = "xs:gYearMonth"
    xs_hexBinary = "xs:hexBinary"
    xs_int = "xs:int"
    xs_integer = "xs:integer"
    xs_long = "xs:long"
    xs_negativeInteger = "xs:negativeInteger"
    xs_nonNegativeInteger = "xs:nonNegativeInteger"
    xs_nonPositiveInteger = "xs:nonPositiveInteger"
    xs_positiveInteger = "xs:positiveInteger"
    xs_short = "xs:short"
    xs_string = "xs:string"
    xs_time = "xs:time"
    xs_unsignedByte = "xs:unsignedByte"
    xs_unsignedInt = "xs:unsignedInt"
    xs_unsignedLong = "xs:unsignedLong"
    UnsignedShort = "xs:unsignedShort"
