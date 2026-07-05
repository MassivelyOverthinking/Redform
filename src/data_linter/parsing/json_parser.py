#########################################################################################################
# IMPORTS
#########################################################################################################

import json

from ...exceptions import JSONParsingError
from typing import Dict, Any
from pathlib import Path

#########################################################################################################
# CUSTOM DATA TYPES
#########################################################################################################

JsonDict = Dict[str, Any]

#########################################################################################################
# JSON PARSING TOOL
#########################################################################################################

# JSON parsing function for Files.
def json_file_parser(filepath: str | Path | None = None) -> JsonDict:
    if filepath is None:
        raise JSONParsingError("A JSON file path must be provided!")
    
    path = Path(filepath)

    if not path.exists():
        raise JSONParsingError(f"JSON filepath doesn't exist: {path}")
    
    if not path.is_file():
        raise JSONParsingError(f"JSON path is not a file: {path}")
    
    if path.suffix.lower() != ".json":
        raise JSONParsingError(f"Expected a JSON file - received: {path.suffix}")
    
    try:
        with path.open("r", encoding="utf-8") as json_file:
            data = json.load(json_file)
    except json.JSONDecodeError as error:
        raise JSONParsingError(
            f"Invalid JSON file: {path} - Line: {error.lineno}, "
            f"column {error.colno} - {error.msg}"
        ) from error
    except OSError as error:
        raise JSONParsingError(f"Failed to read JSON file: {path} - {error}") from error
    
    if not isinstance(data, dict):
        raise JSONParsingError(
            f"JSON file {path} must contain a dictionary"
        )
    
    return data


# JSON parsing function for JSON strings, bytes and bytearrays.
def json_object_parser(json_objec: Dict[str, Any] | str | bytes | bytearray) -> JsonDict:
    if isinstance(json_objec, dict):
        return json_objec
    
    if isinstance(json_objec, (str, bytearray, bytes)):
        try:
            data = json.loads(json_objec)
        except json.JSONDecodeError as error:
            raise JSONParsingError(
                f"Invalid JSON Object - Line {error.lineno}, "
                f"column {error.colno} - {error.msg}"
            ) from error
        
        if not isinstance(data, dict):
            raise JSONParsingError("JSON object must be a top-level dictionary")
        
        return data
    
    raise JSONParsingError(
        "JSON object must be a Dict, JSON string, bytes or bytearray"
    )