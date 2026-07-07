#########################################################################################################
# IMPORTS
#########################################################################################################

from .basemodel import RedformBaseModel
from ..aliases import SourceFormat
from pydantic import Field

#########################################################################################################
# PYDANTIC VALIDATION MODEL -> MATCH (DYNAMIC MATCHING)
#########################################################################################################

class MatchContract(RedformBaseModel):
    dataset_names: list[str] = Field(default_factory=list)
    filename_patterns: list[str] = Field(default_factory=list)
    source_formats: list[SourceFormat] = Field(default_factory=list)

    required_columns: list[str] = Field(default_factory=list)
    optional_columns: list[str] = Field(default_factory=list)
    forbidden_columns: list[str] = Field(default_factory=list)

    column_overlap: float | None = Field(default=None, ge=0, le=1)
    match_score: float = Field(default=0.75, ge=0, le=1)
    priority: float = Field(default=0, ge=0)