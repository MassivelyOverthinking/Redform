#########################################################################################################
# IMPORTS
#########################################################################################################

from typing import Literal

from pydantic import BaseModel, Field, ConfigDict, model_validator

#########################################################################################################
# PYDANTIC VALIDATION MODEL -> COLUMNS
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

class ColumnContract(BaseModel):
    model_config = ConfigDict(extra="forbid")

    type: ColumnTypes
    required: bool = True
    nullable: bool = True
    unique: bool = False

    min: int | float | None = None
    max: int | float | None = None

    min_length: int | None = None
    max_length: int | None = None
    regex: str | None = None

    allowed_values = list[str | int | float | bool] | None = None

    max_null_ratio: float | None = Field(default=None, ge=0, le=1)
    max_duplicate_ratio: float | None = Field(default=None, ge=0, le=1)