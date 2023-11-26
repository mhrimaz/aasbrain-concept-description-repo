from enum import Enum
from typing import Any, List, Optional, Union, Literal

import pydantic
from pydantic import BaseModel, Field, constr

from app.models.has_data_specification import HasDataSpecification
from app.models.has_kind import HasKind
from app.models.has_semantics import HasSemantics
from app.models.identifiable import Identifiable
from app.models.model_type import ModelType
from app.models.multi_language_property import MultiLanguageProperty
from app.models.property import Property
from app.models.qualifable import Qualifiable
from app.models.reference import Reference
from app.models.submodel_element import SubmodelElement


class Submodel(Identifiable, HasKind, HasSemantics, Qualifiable, HasDataSpecification):
    # submodelElements: Optional[List[SubmodelElementChoice]] = Field(
    #     None, min_items=0, discriminator="modelType"
    # )
    # pydantic is not so nice with polymorphism so I can't simply say array of SubmodelElements
    submodelElements: List[Union[Property, MultiLanguageProperty]] = Field(None, min_length=0, discriminator="modelType")

    modelType: ModelType = ModelType.Submodel
