#########################################################################################################
# IMPORTS
#########################################################################################################

from .basemodel import RedformBaseModel
from ..aliases import (
    SeverityTypes
)
from pydantic import Field, model_validator

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

    required_columns: list[str] = Field(default_factory=list)
    forbidden_columns: list[str] = Field(default_factory=list)
    max_null_ratio: float | None = Field(default=None, ge=0, le=1)
    max_duplicate_ratio: float | None = Field(default=None, ge=0, le=1)

    deadstop: bool = False
    severity_threshold: SeverityTypes = "error"
    max_memory: int | float | None = Field(default=None, ge=0)

    @model_validator(mode="after")
    def validate_row_bounds(self) -> "DatasetContract":
        if self.exact_rows is not None:
            if self.min_rows is not None and self.exact_rows < self.min_rows:
                raise ValueError("exact_rows cannot be less than min_rows")

            if self.max_rows is not None and self.exact_rows > self.max_rows:
                raise ValueError("exact_rows cannot be greater than max_rows")

        if self.min_rows is not None and self.max_rows is not None:
            if self.min_rows > self.max_rows:
                raise ValueError("min_rows cannot be greater than max_rows")

        return self

    @model_validator(mode="after")
    def validate_column_bounds(self) -> "DatasetContract":
        if self.exact_columns is not None:
            if self.min_columns is not None and self.exact_columns < self.min_columns:
                raise ValueError("exact_columns cannot be less than min_columns")

            if self.max_columns is not None and self.exact_columns > self.max_columns:
                raise ValueError("exact_columns cannot be greater than max_columns")

        if self.min_columns is not None and self.max_columns is not None:
            if self.min_columns > self.max_columns:
                raise ValueError("min_columns cannot be greater than max_columns")
            
        return self