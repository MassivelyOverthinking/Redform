#########################################################################################################
# IMPORTS
#########################################################################################################

import yaml

from ...exceptions import YAMLParsingError                                          # Custom Exceptions
from ...aliases import ParsedDict, OptionalFilepath, ParsingObject                   # Custom TypeAliases
from pathlib import Path

#########################################################################################################
# YAML PARSING TOOL
#########################################################################################################

#YAML parsing function for Files.
def yaml_file_parser(filepath: OptionalFilepath = None) -> ParsedDict:
    if filepath is None:
        raise YAMLParsingError("A YAML file path must be provided!")
    
    path = Path(filepath)

    if not path.exists():
        raise YAMLParsingError(f"YAML filepath doesn't exist: {path}")
    
    if not path.is_file():
        raise YAMLParsingError(f"YAML path is not a file: {path}")
    
    if path.suffix.lower() not in {".yaml", ".yml"}:
        raise YAMLParsingError(f"Expected a YAML file - received: {path.suffix}")
    
    try:
        with path.open("r", encoding="utf-8") as yaml_file:
            data = yaml.safe_load(yaml_file)
    except yaml.YAMLError as error:
        raise YAMLParsingError(f"Invalid YAML in file: {path} - {error}") from error
    except OSError as error:
        raise YAMLParsingError(f"Failed to read YAML file: {path} - {error}") from error
    
    if not isinstance(data, dict):
        raise YAMLParsingError(
            f"YAML file {path} must contain a dictionary"
        )
    
    return data

# YAML parsing function for JSON strings, bytes and bytearrays.
def yaml_object_parser(yaml_object: ParsingObject) -> ParsedDict:
    if isinstance(yaml_object, dict):
        return yaml_object

    if isinstance(yaml_object, (str, bytes, bytearray)):
        try:
            data = yaml.safe_load(yaml_object)
        except yaml.YAMLError as error:
            raise YAMLParsingError(f"Invalid YAML object: {error}") from error

        if data is None:
            raise YAMLParsingError("YAML object is empty.")

        if not isinstance(data, dict):
            raise YAMLParsingError("YAML object must be a top-level dictionary.")

        return data

    raise YAMLParsingError(
        "yaml_object must be a dict, YAML string, bytes, or bytearray."
    )