"""
Data loading and column validation for the Philippine Customs 2015 program.

Two standalone functions:
    - load_data(): reads the raw CSV into a DataFrame, handling a missing
      file with a clear message and nonzero exit.
    - validate_required_columns(): checks that every column the rest of the
      pipeline depends on is actually present, handling a missing column
      with a clear message and nonzero exit.

Both are imported into main.py and used before any filtering/processing
happens.
"""

from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

import config


def load_data(
    input_path: Path = config.INPUT_PATH,
    encoding: str = config.CSV_ENCODING,
) -> pd.DataFrame:
    """
    Load the raw customs CSV into a DataFrame.

    Parameters
    ----------
    input_path: Path to the CSV file. Defaults to config.INPUT_PATH.
    encoding: Text encoding to use when reading the file. Defaults to
        config.CSV_ENCODING, since this dataset contains non-UTF-8 bytes.

    Returns
    -------
    pd.DataFrame: the raw, unfiltered data exactly as read from disk.

    Exits
    -----
    Exits with status 1 and a clear message if the file does not exist,
    per the assignment's required "missing file" error case.
    """
    if not input_path.exists():
        print(
            f"ERROR: input file not found at '{input_path}'. "
            f"Download 2015.csv from the BetterGov.PH Customs collection "
            f"and place it there before running main.py.",
            file=sys.stderr,
        )
        sys.exit(1)

    df = pd.read_csv(input_path, encoding=encoding, low_memory=False)
    return df


def validate_required_columns(
    df: pd.DataFrame,
    required_columns: set[str] = config.REQUIRED_COLUMNS,
) -> bool:
    """
    Check that every required column is present in the DataFrame.

    Parameters
    ----------
    df: The DataFrame to check (typically the output of load_data()).
    required_columns: Column names that must be present. Defaults to
        config.REQUIRED_COLUMNS.

    Returns
    -------
    bool: True if all required columns are present.

    Exits
    -----
    Exits with status 1 and a clear message listing the missing column(s),
    per the assignment's required "missing required column" error case.
    """
    missing = required_columns - set(df.columns)
    if missing:
        print(
            f"ERROR: required column(s) missing from the dataset: "
            f"{sorted(missing)}. Found columns: {sorted(df.columns)}.",
            file=sys.stderr,
        )
        sys.exit(1)

    return True