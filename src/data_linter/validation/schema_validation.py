#########################################################################################################
# IMPORTS
#########################################################################################################

import polars as pl

from ..utility import _collect_schema_lf
from ..contracts import ColumnContract, DatasetContract
from ..reporting import SchemaReport

#########################################################################################################
# VALIDATION MODULE: POLARS SCHEMA
#########################################################################################################

class SchemaValidator():

    __slots__ = ("schema", "dataset_rules")

    def __init__(self, column_contracts: dict[str, ColumnContract], dataset_contract: DatasetContract):
        self.schema = self._schema_extraction_from_contract(column_contracts)
        self.dataset_rules = self._rules_extraction_from_contract(dataset_contract)

    def _validate_schema(self, schema: pl.Schema) -> SchemaReport:
        pass

    def _schema_extraction_from_contract(column_contracts: dict[str, ColumnContract]) -> dict[str, str]:
        if not isinstance(column_contracts, dict):
            raise TypeError(f"Column Contracts must be of Type: Dict[str, ColumnContract] - Received {type(column_contracts)}")
    
        return {
            key: value.type for key, value in column_contracts.items()
        }
    
    def _rules_extraction_from_contract(rules: DatasetContract) -> dict[str, any]:
        if not isinstance(rules, DatasetContract):
            raise TypeError(f"Rules must be of Type: DatasetContract - Received {type(DatasetContract)}")
        
        return {
            "min_columns": rules.min_columns if not None else None,
            "max_columns": rules.max_columns if not None else None,
            "exact_columns": rules.exact_columns if not None else None,
            "min_rows": rules.min_rows if not None else None,
            "max_rows": rules.max_rows if not None else None,
            "exact_rows": rules.exact_rows if not None else None,
        }
