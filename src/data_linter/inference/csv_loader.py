#########################################################################################################
# IMPORTS
#########################################################################################################

from polars import LazyFrame, scan_csv
from pathlib import Path

#########################################################################################################
# DATA LOADER --> CSV
#########################################################################################################

def _csv_loader(
    filepath: str | Path,
    delimiter: str = ",",
    encoding: str = "utf-8",
    has_header: bool = False,
    quote_char: str = '"',
    try_parse_date: bool = True
) -> LazyFrame:
    if not isinstance(filepath, (str, Path)):
        raise TypeError(f"Filepath must be of Type: Str | Path - Received: {filepath}")
    if not isinstance(delimiter, str):
        raise TypeError(f"Delimiter must be of Type: Str - Received: {delimiter}")
    if not isinstance(encoding, str):
        raise TypeError(f"Encoding must be of Type: Str - Received: {encoding}")
    if not isinstance(has_header, bool):
        raise TypeError(f"Has_header must be of Type: Bool - Received: {has_header}")
    if not isinstance(quote_char, str):
        raise TypeError(f"Quote_char must be of Type: Str - Received: {quote_char}")
    if not isinstance(try_parse_date, bool):
        raise TypeError(f"Try_parse_date must be of Type: Bool - Received: {try_parse_date}")
    
    if isinstance(filepath, str):
        filepath = Path(filepath)

    if not filepath.is_file():
        raise ValueError(f"Filepath does not reference an actual file: {filepath}")
    
    return scan_csv(
        source=filepath, 
        separator=delimiter, 
        encoding=encoding, 
        has_header=has_header, 
        quote_char=quote_char,
        try_parse_dates=True
    )