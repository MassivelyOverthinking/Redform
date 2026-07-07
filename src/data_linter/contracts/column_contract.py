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
# PYDANTIC VALIDATION MODEL -> COLUMNS
#########################################################################################################

class ColumnContract(RedformBaseModel):

    # Standard type anc checks
    type: ColumnTypes
    required: bool = True                               # Is the Column required to be present.
    nullable: bool = True                               # Can values in the column be Null or NaN
    allow_empty: bool = False                           # Can values in the column be empty
    unique: bool = False                                # Are values required to be unique

    # Integer & Float checks
    min: int | float | None = None                      # Minimum integer/float value
    max: int | float | None = None                      # Maximum integer/float value
    exclusive_min: bool = False                         # Does maximum check include the specified value
    exclusive_max: bool = False                         # Does minimum check include the specified value

    # Statistical checks
    mean_min: int | float | None = None                             # Mean minimum of the entire column values
    mean_max: int | float | None = None                             # Mean maximum of the entire column values
    std_min: int | float | None = Field(default=None, ge=0)         # Standard deviation minimum of the entire column values
    std_max: int | float | None = Field(default=None, ge=0)         # Standard deviation maximum of the entire column values

    # String length check
    min_length: int | None = Field(default=None, ge=0)              # Minimum length required by column values
    max_length: int | None = Field(default=None, ge=0)              # Maximum length required by column values
    exact_length: int | None = Field(default=None, ge=0)            # Exact length required by column values

    # String & Pattern checks
    regex: str | None = None                            # RegEx string check
    starts_with: str | None = None                      # Check each value in the column begins with a certain value (prefix)
    ends_with: str | None = None                        # Check each value in the column ends with a certain value (suffix)
    contains: str | None = None                         # Check each value in the column contains the specified value
    not_contains: str | None = None                     # Check each value in the column does not contain the specified value

    # Datetime & Data checks
    min_date: DateValue | None = None                   # Minimum date for each value in the column
    max_date: DateValue | None = None                   # Maximum date for each value in the column
    not_future: bool = False                            # Ensures that datatime, date and string values can't specify a date in the future
    not_past: bool = False                              # Ensures that datatime, date and string values can't specify a date in the past
    format: str | None = None                           # Enforces column wide datetime and date formatting
    weekdays: list[Weekdays] | None = None              # ENUMS: Check values present against examples in the pre-approved array

    # Value & Enum checks
    allowed_values: list[ScalarValue] | None = None                     # ENUMS: Check values present against examples in the pre-approved array
    forbidden_values: list[ScalarValue] | None = None                   # ENUMS: Check values present against examples in the pre-approved array
    min_distinct_values: int | None = Field(default=None, ge=0)         # Minimum number of distinct values in column
    max_distinct_values: int | None = Field(default=None, ge=0)         # Maximum number of distinct values in column

    # Ratio checks
    max_null_ratio: float | None = Field(default=None, ge=0, le=1)      # Check the ratio of null values against the complate column
    max_duplicate_ratio: float | None = Field(default=None, ge=0, le=1) # Check the ratio of duplicate values against the complate column

    # General validations
    trim_whitespace: bool = True                        # Ensure that all values in columns have their whitespace trimmed
    severity: SeverityTypes = "error"                   # Severity levels for checking and final reporting
    decimals: int | None = Field(default=None, ge=0)    # Number of decimals allowed by floats in the column
    coerce_string: bool = False                         # Coerce other date types into String-types
    deadstop: bool = False                              # Stop processing immediately if any step fails
    description: str | None = None                      # Optional description for the column data

    @field_validator("regex")
    @classmethod
    def validate_regex(cls, value: str | None) -> str | None:
        if value is None:
            return value
        
        import re

        try:
            re.compile(value)
        except re.error as error:
            raise ValueError(f"Invalid RegEx pattern: {error}") from error
        
        return value
    
    @field_validator("weekdays", mode="before")
    @classmethod
    def normalize_weekdays(cls, value: Any) -> Any:
        if value is None:
            return value
        if not isinstance(value, list):
            raise ValueError("weekdays must be a List of weekday names")
        
        return [str(item).lower() for item in value]

    @model_validator(mode="after")
    def validate_min_max(self) -> "ColumnContract":
        if self.min is not None and self.max is not None and self.min > self.max:
            raise ValueError("Min value cannot be greater than Max")
        
        if self.mean_min is not None and self.mean_max is not None:
            if self.mean_min > self.mean_max:
                raise ValueError("mean_min cannot be greater that mean_max")
            
        if self.std_min is not None and self.std_max is not None:
            if self.std_min > self.std_max:
                raise ValueError("std_min cannot be greater that std_max")
        
        return self
    
    @model_validator(mode="after")
    def validate_string_length(self) -> "ColumnContract":
        if self.min_length is not None and self.max_length is not None:
            if self.min_length > self.max_length:
                raise ValueError("min_length cannot be greater than max_length")
            
        if self.exact_length is not None:
            if self.min_length is not None and self.exact_length < self.min_length:
                raise ValueError("exact_length cannot be less than min_length")

            if self.max_length is not None and self.exact_length > self.max_length:
                raise ValueError("exact_length cannot be greater than max_length")
            
        return self
    
    @model_validator(mode="after")
    def validate_date_bounds(self) -> "ColumnContract":
        if self.not_future and self.not_past:
            raise ValueError("not_future and not_past cannot be True at the same time")
        
        if self.min_date is not None and self.max_date is not None:
            min_date = self._coerce_date_like(self.min_date)
            max_date = self._coerce_date_like(self.max_date)

            if min_date > max_date:
                raise ValueError("min_distance cannot be greater than max_date")
            
        return self
    
    @model_validator(mode="after")
    def validate_allowed_and_forbidden_values(self) -> "ColumnContract":
        if self.allowed_values is not None and len(self.allowed_values) == 0:
            raise ValueError("allowed_values cannot be an empty list")

        if self.forbidden_values is not None and len(self.forbidden_values) == 0:
            raise ValueError("forbidden_values cannot be an empty list")

        if self.allowed_values is not None and self.forbidden_values is not None:
            overlap = set(self.allowed_values).intersection(self.forbidden_values)

            if overlap:
                raise ValueError(
                    f"allowed_values and forbidden_values overlap: {sorted(overlap)}"
                )

        return self
    
    @model_validator(mode="after")
    def validate_type_specific_fields(self) -> "ColumnContract":
        numeric_fields = {
            "min": self.min,
            "max": self.max,
            "mean_min": self.mean_min,
            "mean_max": self.mean_max,
            "std_min": self.std_min,
            "std_max": self.std_max,
            "decimals": self.decimals,
        }

        string_fields = {
            "min_length": self.min_length,
            "max_length": self.max_length,
            "exact_length": self.exact_length,
            "regex": self.regex,
            "starts_with": self.starts_with,
            "ends_with": self.ends_with,
            "contains": self.contains,
            "not_contains": self.not_contains,
        }

        date_fields = {
            "min_date": self.min_date,
            "max_date": self.max_date,
            "not_future": self.not_future,
            "not_past": self.not_past,
            "format": self.format,
            "weekdays": self.weekdays,
        }

        if self.type not in {"int", "float"}:
            self._reject_configured_fields("numeric", numeric_fields)

        if self.type != "float" and self.decimals is not None:
            raise ValueError("decimals can only be used with type='float'")

        if self.type not in {"string", "category"}:
            self._reject_configured_fields("string", string_fields)

        if self.type not in {"date", "datetime"}:
            self._reject_configured_fields("date/datetime", date_fields)

        return self

    @staticmethod
    def _coerce_date_like(value: DateValue) -> date | datetime:
        if isinstance(value, (date, datetime)):
            return value

        if isinstance(value, str):
            try:
                return datetime.fromisoformat(value)
            except ValueError as error:
                raise ValueError(
                    f"Date value must be ISO formatted, received: {value!r}"
                ) from error

        raise ValueError(f"Invalid date-like value: {value!r}")
    
    @staticmethod
    def _reject_configured_fields(
        field_group_name: str,
        fields: dict[str, Any],
    ) -> None:
        configured = [
            field_name
            for field_name, field_value in fields.items()
            if field_value is not None and field_value is not False
        ]

        if configured:
            raise ValueError(
                f"{field_group_name} checks are not valid for this column type: "
                f"{', '.join(configured)}"
            )