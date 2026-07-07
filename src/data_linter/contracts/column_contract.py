#########################################################################################################
# IMPORTS
#########################################################################################################

from typing import Literal
from datetime import datetime, date

from ..exceptions import ValidationError
from .basemodel import RedformBaseModel
from pydantic import Field, model_validator

#########################################################################################################
# CUSSTOM DATA LITERALS
#########################################################################################################

ColumnTypes = Literal[
    "string",
    "int",
    "float",
    "bool",
    "date",
    "datetime",
    "category",
]

SeverityTypes = Literal[
    "error",
    "warning",
    "debug",
    "info"
]

#########################################################################################################
# PYDANTIC VALIDATION MODEL -> COLUMNS
#########################################################################################################

class ColumnContract(RedformBaseModel):

    # Standard type anc checks
    type: ColumnTypes
    required: bool = True
    nullable: bool = True
    allow_empty: bool = False
    unique: bool = False

    # Integer & Float checks
    min: int | float | None = None
    max: int | float | None = None
    exclusive_min: bool = False
    exclusive_max: bool = False
    std: int | float | None = None

    # String length check
    min_length: int | None = None
    max_length: int | None = None
    exact_length: int | None = None

    # String & Pattern checks
    regex: str | None = None
    starts_with: str | None = None
    ends_with: str | None = None
    contains: str | None = None
    not_contains: str | None = None

    # Datetime & Data checks
    min_date: datetime | date | str | None = None
    max_date: datetime | date | str | None = None
    not_future: bool = False
    not_past: bool = False
    format: str | None = None
    weekdays: list[str] | None = None

    # Value & Enum checks
    allowed_values = list[str | int | float | bool] | None = None
    fordbidden_values = list[str | int | float | bool] | None = None

    # Ratio checks
    max_null_ratio: float | None = Field(default=None, ge=0, le=1)
    max_duplicate_ratio: float | None = Field(default=None, ge=0, le=1)

    # General validations
    trim_whitespace: bool = True
    severity: SeverityTypes | None = None
    decimals: int | None = None
    coerce_string: bool = False
    deadstop: bool = False

    @model_validator(mode="after")
    def validate_min_max(self) -> "ColumnContract":
        if self.min is not None and self.max is not None and self.min > self.max:
            raise ValidationError("Min value cannot be greater than Max")
        if self.min_length is not None and self.max_length is not None and self.min_length > self.max_length:
            raise ValidationError("Min lenght cannot be greater than Max length")