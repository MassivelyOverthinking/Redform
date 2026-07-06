#########################################################################################################
# IMPORTS
#########################################################################################################

from typing import Dict, Any, TypeAlias
from pathlib import Path

#########################################################################################################
# CUSTOM DATA TYPES
#########################################################################################################

ParsedDict = Dict[str, Any]                                                 # Dictionary struct --> Used for handling output results in parsing module

FilePath: TypeAlias = str | Path                                            # Path struct --> Used for handling input filepath in parsing module
OptionalFilepath: TypeAlias = FilePath | None                               # Path struct --> Wrapper for FilePath alias to include 'None' functionality

ParsingObject: TypeAlias = Dict[str, Any] | str | bytes | bytearray         # Object struct --> Used for handling input in object parsing modules