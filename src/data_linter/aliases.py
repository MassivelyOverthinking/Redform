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

ColumnTypes: TypeAlias = Literal[                                           # Column struct --> Determines the data type associated with columns
    "string",
    "int",
    "float",
    "bool",
    "date",
    "datetime",
    "category",
]

SeverityTypes: TypeAlias = Literal[                                         # Severity struct --> Used for determining the severity of Pydantic validation model
    "error",
    "warning",
    "debug",
    "info"
]

Weekdays: TypeAlias = Literal[                                              # Date struct --> Simple list of individual weekdays for date handling
    "monday",
    "tuesday",
    "wednesday",
    "thursday",
    "friday",
    "saturday",
    "sunday",
]

SourceFormat: TypeAlias = Literal[                                          # File Extensions --> All current supported file extensions formats
    "csv",
    "parquet",
    "json"
]

MemoryMode: TypeAlias = Literal[                                            # Memory Modes --> Supported memory estimation modes
    "full",
    "summary"
]

ScalarValue: TypeAlias = str | int | float | bool                           # Type struct --> Typing for handling core dtype features

DateValue: TypeAlias = datetime | date | str                                # Date struct --> Typing for handling core date/datetime features

TargetType: TypeAlias = Literal["regression", "classification"]             # ML struct --> All current supported ML/AI operations for target validation

NumericColumn: TypeAlias = Literal["int", "float"]                         

StringColumn: TypeAlias = Literal["string", "category"]

DateColumn: TypeAlias = Literal["datetime", "date"]

#########################################################################################################
# CUSTOM DATA TYPES & ALIASES --> FILE LOADERS
#########################################################################################################

PolarsSchema: TypeAlias = dict[str, pl.DataType]

ParquetStrategy: TypeAlias = Literal[
    "auto",
    "columns",
    "row_groups",
    "prefiltered",
    "none",
]

#########################################################################################################
# CUSTOM DATA TYPES & ALIASES --> SCHEMA VALIDATION
#########################################################################################################

SchemaCheckResult: TypeAlias = dict[str, Any]