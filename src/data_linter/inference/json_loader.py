#########################################################################################################
# IMPORTS
#########################################################################################################

from ..aliases import PolarsSchema

from polars import LazyFrame, scan_ndjson
from pathlib import Path

#########################################################################################################
# DATA LOADER --> JSON
#########################################################################################################

JSON_SUFFIXES = [".ndjson", ".jsonl"]

def _ndjson_loader(
    filepath: str | Path,
    schema: PolarsSchema | None = None,
    schema_overrides: PolarsSchema | None = None,
    infer_schema_length: int | None = 100,
    batch_szie: int | None = None,
    n_rows: int | None = None,
    row_index_name: str | None = None,
    row_index_offset: int = 0,
    low_memory: bool = False,
    rechunk: bool = False,
    ignore_errors: bool = False
) -> LazyFrame:
    if not isinstance(filepath, (str, Path)):
        raise TypeError(f"Filepath must be of Type: Str | Path - Received: {filepath}")
    
    source_path = Path(filepath)

    if not source_path.exists():
        raise ValueError(f"Filepath does not exist as a Path: {source_path}")

    if not source_path.is_file():
        raise ValueError(f"Filepath does not reference an actual file: {source_path}")
    
    path_suffix = source_path.suffix
    if path_suffix.lower() not in JSON_SUFFIXES:
        raise ValueError(f"Expected a JSON file extension but received: {path_suffix}")
    
    return scan_ndjson(
        source=source_path,
        schema=schema,
        schema_overrides=schema_overrides,
        infer_schema_length=infer_schema_length,
        batch_size=batch_szie,
        n_rows=n_rows,
        row_index_name=row_index_name,
        row_index_offset=row_index_offset,
        low_memory=low_memory,
        rechunk=rechunk,
        ignore_errors=ignore_errors
    )