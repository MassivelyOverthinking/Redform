#########################################################################################################
# IMPORTS
#########################################################################################################

from ..aliases import ParquetStrategy

from polars import LazyFrame, scan_parquet
from pathlib import Path

#########################################################################################################
# DATA LOADER --> PARQUET
#########################################################################################################

PARQUET_SUFFIXES = [".parquet", ".pq"]

def _parquet_loader(
    filepath: str | Path,
    n_rows: int | None = None,
    row_index_name: str | None = None,
    row_index_offset: int | None = None,
    parallel: ParquetStrategy = "auto",
    use_statistics: bool = True,
    rechunk: bool = False,
    low_memory: bool = False,
) -> LazyFrame:
    if not isinstance(filepath, (str, Path)):
        raise TypeError(f"Filepath must be of Type: Str | Path - Received: {filepath}")
    
    source_path = Path(filepath)

    if not source_path.exists():
        raise ValueError(f"Filepath does not exist as a Path: {source_path}")

    if not source_path.is_file():
        raise ValueError(f"Filepath does not reference an actual file: {source_path}")
    
    path_suffix = source_path.suffix
    if path_suffix.lower() not in PARQUET_SUFFIXES:
        raise ValueError(f"Expected a Parquet file extension but received: {path_suffix}")
    
    return scan_parquet(
        source=source_path, 
        n_rows=n_rows,
        row_index_name=row_index_name,
        row_index_offset=row_index_offset,
        parallel=parallel,
        use_statistics=use_statistics,
        rechunk=rechunk,
        low_memory=low_memory
    )