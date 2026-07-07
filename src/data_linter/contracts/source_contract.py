#########################################################################################################
# IMPORTS
#########################################################################################################

from .basemodel import RedformBaseModel
from ..aliases import SourceFormat
from pydantic import Field

#########################################################################################################
# PYDANTIC VALIDATION MODEL -> SOURCE
#########################################################################################################

class SourceContract(RedformBaseModel):
    format: SourceFormat | None = None
    encoding: str = "utf-8"
    delimiter: str = ","
    has_header: bool = True
    quote_char: str | None = '"'