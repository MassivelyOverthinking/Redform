#########################################################################################################
# IMPORTS
#########################################################################################################

from typing import Any
from datetime import datetime, date

from .basemodel import RedformBaseModel
from ..aliases import (
    ColumnTypes, SeverityTypes, Weekdays, ScalarValue, DateValue
)
from pydantic import Field, model_validator, field_validator

#########################################################################################################
# PYDANTIC VALIDATION MODEL -> DATASET
#########################################################################################################

class DatasetContract(RedformBaseModel):
    min_rows: int | None = Field(default=None, ge=0)
    max_rows: int | None = Field(default=None, ge=0)
    exact_rows: int | None = Field(default=None, ge=0)

    min_columns: int | None = Field(default=None, ge=0)
    max_columns: int | None = Field(default=None, ge=0)
    exact_columns: int | None = Field(default=None, ge=0)
