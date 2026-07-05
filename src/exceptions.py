#########################################################################################################
# IMPORTS
#########################################################################################################

#########################################################################################################
# CUSTOM EXCEPTIONS/ERRORS
#########################################################################################################

class RedformBaseError(Exception):
    def __init__(self, message: str, code: str = "REDFORM_BASE_ERROR", _details: dict | None = None):
        super().__init__(self.message)
        self.message = message
        self.code = code
        self._details = _details or {}

    def get_details(self) -> str:
        return ", ".join(
            f"{key}={value}" for key, value in self._details.items()
        )

    def __str__(self) -> str:
        return f"{self.code}: {self.message}"