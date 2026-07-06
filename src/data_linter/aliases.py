#########################################################################################################
# IMPORTS
#########################################################################################################

from typing import Dict, Any, TypeAlias
from pathlib import Path

#########################################################################################################
# CUSTOM DATA TYPES
#########################################################################################################

ParsedDict = Dict[str, Any]

FilePath: TypeAlias = str | Path
OptionalFilepath: TypeAlias = FilePath | None

ParsingObject: TypeAlias = Dict[str, Any] | str | bytes | bytearray