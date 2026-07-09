#########################################################################################################
# IMPORTS
#########################################################################################################

import polars as pl

from datetime import date, datetime
from typing import Dict, Any, TypeAlias, Literal
from pathlib import Path

#########################################################################################################
# CUSTOM DATA TYPES & ALIASES --> GENERAL
#########################################################################################################

ParsedDict = Dict[str, Any]                                                 # Dictionary struct --> Used for handling output results in parsing module

FilePath: TypeAlias = str | Path                                            # Path struct --> Used for handling input filepath in parsing module
OptionalFilepath: TypeAlias = FilePath | None                               # Path struct --> Wrapper for FilePath alias to include 'None' functionality

ParsingObject: TypeAlias = Dict[str, Any] | str | bytes | bytearray         # Object struct --> Used for handling input in object parsing modules

#########################################################################################################
# CUSTOM DATA TYPES & ALIASES --> PYDANTIC
#########################################################################################################

ColumnTypes: TypeAlias = Literal[
    "string",
    "int",
    "float",
    "bool",
    "date",
    "datetime",
    "category",
]

SeverityTypes: TypeAlias = Literal[
    "error",
    "warning",
    "debug",
    "info"
]

Weekdays: TypeAlias = Literal[
    "monday",
    "tuesday",
    "wednesday",
    "thursday",
    "friday",
    "saturday",
    "sunday",
]

SourceFormat: TypeAlias = Literal[
    "csv",
    "parquet",
    "json"
]

ScalarValue: TypeAlias = str | int | float | bool

DateValue: TypeAlias = datetime | date | str

TargetType: TypeAlias = Literal["regression", "classification"]

NumericColumn: TypeAlias = Literal["int", "float"]

StringColumn: TypeAlias = Literal["string", "category"]

DateColumn: TypeAlias = Literal["datetime", "date"]


PolarsSchema: TypeAlias = dict[str, pl.DataType]

ParquetStrategy = Literal[
    "auto",
    "columns",
    "row_groups",
    "prefiltered",
    "none",
]