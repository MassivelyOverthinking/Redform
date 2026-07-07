#########################################################################################################
# IMPORTS
#########################################################################################################

#########################################################################################################
# BASE EXCEPTIONS
#########################################################################################################

# Base Error class
class RedformBaseError(Exception):
    def __init__(self, message: str, code: str = "REDFORM_BASE_ERROR", _details: dict | None = None):
        super().__init__(message)
        self.message = message
        self.code = code
        self._details = _details or {}

    # Extract additionbal Error details --> Efficient Error checking/debugging
    def get_details(self) -> str:
        return ", ".join(
            f"{key}={value}" for key, value in self._details.items()
        )

    # OVERRIDE --> Return error message.
    def __str__(self) -> str:
        return f"{self.code}: {self.message}"
    
#########################################################################################################
# PARSING EXCEPTIONS
#########################################################################################################

# Parsing error for primary use in JSON parsing module
# Use the _details attribute for additional information when catching errors --> get_details()
class JSONParsingError(RedformBaseError):
    def __init__(self, message: str, code: str = "JSON_PARSING_ERROR", _details: dict[str, any] | None = None):
        super().__init__(message=message, code=code, _details=_details)

# Parsing error for primary use in YAML parsing module
# Use the _details attribute for additional information when catching errors --> get_details()
class YAMLParsingError(RedformBaseError):
    def __init__(self, message: str, code: str = "YAML_PARSING_ERROR", _details: dict[str, any] | None = None):
        super().__init__(message=message, code=code, _details=_details)

