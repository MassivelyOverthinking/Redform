#########################################################################################################
# IMPORTS
#########################################################################################################

from typing import Literal

from .basemodel import RedformBaseModel
from .metadata_contract import MetadataContract
from .source_contract import SourceContract
from .match_contract import MatchContract
from .target_contract import TargetContract 
from .column_contract import ColumnContract
from .dataset_contract import DatasetContract
from pydantic import Field, model_validator

#########################################################################################################
# PYDANTIC VALIDATION MODEL -> FULL CONTRACT
#########################################################################################################

class Contract(RedformBaseModel):
    dataset: str = Field(min_length=1)
    version: int = Field(default=1, ge=1)
    description: str | None = None

    metadata: MetadataContract | None = None
    source: SourceContract | None = None
    match: MatchContract | None = None

    primary_key: str | list[str] | None = None
    target: TargetContract | None = None

    columns: dict[str, ColumnContract] = Field(default_factory=dict)

    rules: DatasetContract = Field(default_factory=DatasetContract)

    @model_validator(mode="after")
    def validate_contract_columns(self) -> "Contract":
        if len(self.columns) == 0:
            raise ValueError("Contract must contain at least 1 column")
        return self
    
    @model_validator(mode="after")
    def validate_primary_key(self) -> "Contract":
        if self.primary_key is None:
            return self
        
        declared_columns = set(self.columns)

        primary_keys = (
            [self.primary_key]
            if isinstance(self.primary_key, str)
            else self.primary_key
        )

        missing = [column for column in primary_keys if column not in declared_columns]

        if missing:
            raise ValueError(
                f"primary_key references unknown columns: {', '.join(missing)}"
            )

        return self
    
    @model_validator(mode="after")
    def validate_target_contract(self) -> "Contract":
        if self.target is None:
            return self
        
        if self.target.column not in self.columns:
            raise ValueError(f"Target column references uknown column: {self.target.column}")
        
        return self
    
    @model_validator(mode="after")
    def validate_dataset_rules(self) -> "Contract":
        declared_columns = set(self.columns)

        missing_columns = [
            column for column in self.rules.required_columns if column not in declared_columns
        ]

        if missing_columns:
            raise ValueError(f"Required column rules references unknown columns: " + ", ".join(missing_columns))
        
        return self




