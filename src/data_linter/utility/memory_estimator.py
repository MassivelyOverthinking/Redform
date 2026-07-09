#########################################################################################################
# IMPORTS
#########################################################################################################

import polars as pl

#########################################################################################################
# MEMORY ESTIMATION
#########################################################################################################

# Byte size estimations for common Polars Dtypes.
DTYPE_SIZE_ESTIMATIONS = {
    pl.Int8: 1,
    pl.UInt8: 1,
    pl.Boolean: 1,
    pl.Int16: 2,
    pl.UInt16: 2,
    pl.Int32: 4,
    pl.UInt32: 4,
    pl.Float32: 4,
    pl.Date: 4,
    pl.Int64: 8,
    pl.UInt64: 8,
    pl.Float64: 8,
    pl.Datetime: 8,
    pl.Duration: 8
}

def _lazyframe_memory_estimation(lf: pl.LazyFrame) -> float:
    schema = lf.collect_schema()

    summary_exprs: list[pl.Expr] = [
        pl.len().alias("__row_count"),
    ]

    for column_name, dtype in schema.items():
        if dtype == pl.String:
            summary_exprs.append(
                pl.col(column_name)
                .str.len_bytes()
                .mean()
                .alias(f"{column_name}__avg_bytes")
            )

    summary = lf.select(summary_exprs).collect().row(0, named=True)
    row_count = summary["__row_count"]

    estimated_bytes = 0.0

    for column_name, dtype in schema.items():
        if dtype in DTYPE_SIZE_ESTIMATIONS:
            estimated_bytes += row_count * DTYPE_SIZE_ESTIMATIONS[dtype]
        elif dtype == pl.String:
            avg_bytes = summary.get(f"{column_name}__avg_bytes") or 0
            # String columns also need offsets/validity buffers.
            # This is intentionally approximate.
            estimated_bytes += row_count * (avg_bytes + 8)
        else:
            # Fallback for unknown/nested/object-like columns.
            estimated_bytes += row_count * 16

    return estimated_bytes / (1024 * 1024)