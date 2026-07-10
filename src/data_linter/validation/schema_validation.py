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

POLARS_INTEGER_TYPES = [
    pl.Int8,
    pl.Int16,
    pl.Int32,
    pl.Int64,
    pl.Int128,
    pl.UInt8,
    pl.UInt16,
    pl.UInt32,
    pl.UInt64,
    pl.UInt128
]

POLARS_FLOAT_TYPES = [
    pl.Float16,
    pl.Float32,
    pl.Float64,
    pl.Decimal
]

POLARS_TEMPORAL_TYPES = [
    pl.Duration,
    pl.Date,
    pl.Datetime,
    pl.Time,
]

POLARS_STRING_TYPES = [
    pl.String,
    pl.Utf8
]

POLARS_CATEGORY_TYPES = [
    pl.Categorical,
    pl.Enum
]

class SchemaValidator():

    __slots__ = ("schema", "dataset_rules", "_frozen")

    def __init__(self, column_contracts: dict[str, ColumnContract], dataset_contract: DatasetContract):
        self.schema = self._schema_extraction_from_contract(column_contracts)
        self.dataset_rules = self._rules_extraction_from_contract(dataset_contract)
        self._frozen = True

    # Main validation method --> Produces a finalized SchemaReport
    def validate(self, schema: pl.Schema) -> SchemaReport:
        if not isinstance(schema, pl.Schema):
            raise TypeError(f"Schema must be of Type: Polars Dataframe - Received {type(schema)}")
        
    # Validates the Schema against the Column & Dataset Contract
    def _validate_schema(self, schema: pl.Schema) -> None:
        if not isinstance(schema, pl.Schema):
            raise TypeError(f"Schema must be of Type: Polars Dataframe - Received {type(schema)}")
        
        results = {}
        forbidden_columns: list = self.dataset_rules["forbidden_columns"]
        required_columns: list = self.dataset_rules["required_columns"]

        schema_fails = 0
        schema_passes = 0

        for column_name, column_type in self.schema.items():
            if column_name in forbidden_columns:
                results[column_name] = f"Column: {column_name} is a forbidden column!"
                schema_fails += 1
            else:
                received_type: pl.DataType = schema[column_name]
                if self._check_datatype(column_type, received_type):
                    results[column_name] = self._create_info_str(False, column_name, column_type, received_type)
                    schema_passes += 1
                else:
                    results[column_name] = self._create_info_str(True, column_name, column_type, received_type)
                    schema_fails += 1

    # Helper-method for creating a information string
    def _create_info_str(self, failure: bool, column_name: str, expected_type: str, given_type: pl.DataType) -> str:
        if failure:
            return f"FAIL | Column: {column_name}, has the incorrect typing - Expected: {expected_type} | Received: {given_type}"
        
        return f"PASS | Column: {column_name}, has the correct typing - {expected_type}"

    # Helper-method for checking if the expected datatype matches received datatypes.
    def _check_datatype(self, expected_type: str, given_type: pl.DataType) -> bool:
        if not isinstance(expected_type, str):
            raise TypeError(f"Expected type must be of Type: Str - Recevied {type(expected_type)}")
        if not isinstance(given_type, pl.DataType):
            raise TypeError(f"Given type must be of Type: Polars Datatype - Recevied {type(given_type)}")
        
        match expected_type.lower():
            case "string":
                return given_type in POLARS_STRING_TYPES
            case "int":
                return given_type in POLARS_INTEGER_TYPES
            case "float":
                return given_type in POLARS_FLOAT_TYPES
            case "datetime":
                return given_type == pl.Datetime
            case "data":
                return given_type == pl.Date
            case "category":
                return given_type in POLARS_CATEGORY_TYPES
            case _:
                return False

    # Initialization method --> Extracts the necessary data from ColumnContracts
    def _schema_extraction_from_contract(column_contracts: dict[str, ColumnContract]) -> dict[str, str]:
        if not isinstance(column_contracts, dict):
            raise TypeError(f"Column Contracts must be of Type: Dict[str, ColumnContract] - Received {type(column_contracts)}")
    
        return {
            key: value.type for key, value in column_contracts.items()
        }
    
    # Initialization method --> Extracts the necessary data from DatasetContract
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
            "required_columns": rules.required_columns if not None else None,
            "forbidden_columns": rules.forbidden_columns if not None else None,
        }
    
    # Freeze class attributes for immutability.
    def __setattr__(self, new: any, old: any):
        if getattr(self, "_frozen", False):
            raise AttributeError(f"Cannot modify frozen attribute: {new}")
