from enum import Enum
from typing import Any, List, Optional, Union, Literal
from pydantic import BaseModel, Field, constr

from app.models.asset_information import AssetInformation
from app.models.has_data_specification import HasDataSpecification
from app.models.identifiable import Identifiable
from app.models.reference import Reference

class AssetAdministrationShell(Identifiable, HasDataSpecification):
    derivedFrom: Optional[Reference] = None
    assetInformation: AssetInformation
    submodels: Optional[List[Reference]] = Field(None, min_items=1)
    modelType: str = Field("AssetAdministrationShell", const=True)