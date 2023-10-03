from enum import Enum
from typing import Any, List, Optional, Union, Literal

from pydantic import BaseModel, Field, constr


class DataTypeDefXsd(Enum):
    xs_anyURI = 'xs:anyURI'
    xs_base64Binary = 'xs:base64Binary'
    xs_boolean = 'xs:boolean'
    xs_byte = 'xs:byte'
    xs_date = 'xs:date'
    xs_dateTime = 'xs:dateTime'
    xs_decimal = 'xs:decimal'
    xs_double = 'xs:double'
    xs_duration = 'xs:duration'
    xs_float = 'xs:float'
    xs_gDay = 'xs:gDay'
    xs_gMonth = 'xs:gMonth'
    xs_gMonthDay = 'xs:gMonthDay'
    xs_gYear = 'xs:gYear'
    xs_gYearMonth = 'xs:gYearMonth'
    xs_hexBinary = 'xs:hexBinary'
    xs_int = 'xs:int'
    xs_integer = 'xs:integer'
    xs_long = 'xs:long'
    xs_negativeInteger = 'xs:negativeInteger'
    xs_nonNegativeInteger = 'xs:nonNegativeInteger'
    xs_nonPositiveInteger = 'xs:nonPositiveInteger'
    xs_positiveInteger = 'xs:positiveInteger'
    xs_short = 'xs:short'
    xs_string = 'xs:string'
    xs_time = 'xs:time'
    xs_unsignedByte = 'xs:unsignedByte'
    xs_unsignedInt = 'xs:unsignedInt'
    xs_unsignedLong = 'xs:unsignedLong'
    xs_unsignedShort = 'xs:unsignedShort'
