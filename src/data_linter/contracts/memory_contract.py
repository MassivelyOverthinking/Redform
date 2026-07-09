#########################################################################################################
# IMPORTS
#########################################################################################################

from .basemodel import RedformBaseModel
from pydantic import Field

from ..aliases import MemoryMode, SeverityTypes

#########################################################################################################
# PYDANTIC VALIDATION MODEL -> MEMORY
#########################################################################################################

class MemoryContract(RedformBaseModel):
    mode: MemoryMode = "summary"
    max_total_mb: int | float | None = Field(default=None, ge=0)
    severity: SeverityTypes = "info"