#########################################################################################################
# IMPORTS
#########################################################################################################

from .basemodel import RedformBaseModel
from pydantic import Field

#########################################################################################################
# PYDANTIC VALIDATION MODEL -> METADATA
#########################################################################################################

class MetadataContract(RedformBaseModel):
    owner: str | None = None
    domain: str | None = None
    description: str | None = None
    tags: list[str] | None = Field(default_factory=list)