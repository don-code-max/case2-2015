"""
Configuration for the Philippine Customs 2015 data summary program.

Holds the input path, filter values, grouping columns, and output folder
so the rest of the program (loader, processing, aggregation, plotting)
reads from a single source of truth instead of hardcoding values.
"""

from pathlib import Path

# --- Paths ---------------------------------------------------------------

INPUT_PATH: Path = Path("data/2015.csv")
OUTPUT_DIR: Path = Path("outputs")

# The uploaded/verified copy of this file has:
#   rows: 2,236,612 (+1 header row)
#   columns: 30
#   dutiablevaluephp total: PHP 3,587,267,375,257
#   sha256: b3b5a3a95340179a716a05611d51ad4906484d38363d1ac36494a404c04e4370
CSV_ENCODING: str = "latin1"  # file contains non-UTF-8 bytes (e.g. in goodsdescription)

# --- Required columns ------------------------------------------------------

REQUIRED_COLUMNS: set[str] = {
    "tq",
    "countryorigin_iso3",
    "dutiablevaluephp",
}

# --- Filter (two conditions, combined with .loc) --------------------------
# Rule: keep rows from Q4 2015 with a positive dutiable value.
# Rows with a missing filter value (tq or dutiablevaluephp is null) are
# routed to the "excluded" group, not silently dropped — see audit_log.csv.

FILTER_QUARTER: str = "2015q4"
FILTER_MIN_VALUE: float = 0.0  # dutiablevaluephp must be strictly greater than this

# --- Grouping / measure -----------------------------------------------------

CATEGORY_COLUMN_1: str = "countryorigin_iso3"
CATEGORY_COLUMN_2: str = "tq"
MEASURE_COLUMN: str = "dutiablevaluephp"

# --- Derived columns ---------------------------------------------------------

DERIVED_NUMERIC_COLUMN: str = "dutiablevaluephp_million"
DERIVED_NUMERIC_DIVISOR: float = 1_000_000.0

DERIVED_FLAG_COLUMN: str = "value_tier"
# Threshold is computed at runtime as the median of MEASURE_COLUMN on the
# filtered data (see src/processing.py) rather than fixed here, so it
# reflects the actual filtered distribution.
VALUE_TIER_HIGH_LABEL: str = "high"
VALUE_TIER_LOW_LABEL: str = "low"

# --- Validation tolerances ---------------------------------------------------

# Absolute tolerance (in PHP) for comparing dutiablevaluephp sums.
VALIDATION_ABS_TOLERANCE: float = 1.0
VALIDATION_REL_TOLERANCE: float = 0.0

# Reference totals supplied by the assignment for Customs 2015 (whole file,
# before filtering) — used only for the raw-load validation check.
REFERENCE_ROW_COUNT: int = 2_236_612
REFERENCE_COLUMN_COUNT: int = 30
REFERENCE_DUTIABLEVALUEPHP_SUM: float = 3_587_267_375_257.0

# --- Config dict -----------------------------------------------------------
# Required by the assignment: "a configuration dictionary". Built from the
# values above so there's one source of truth, not two.

CONFIG: dict = {
    "input_path": str(INPUT_PATH),
    "output_dir": str(OUTPUT_DIR),
    "encoding": CSV_ENCODING,
    "required_columns": REQUIRED_COLUMNS,
    "filter_quarter": FILTER_QUARTER,
    "filter_min_value": FILTER_MIN_VALUE,
    "category_column_1": CATEGORY_COLUMN_1,
    "category_column_2": CATEGORY_COLUMN_2,
    "measure_column": MEASURE_COLUMN,
    "derived_numeric_column": DERIVED_NUMERIC_COLUMN,
    "derived_numeric_divisor": DERIVED_NUMERIC_DIVISOR,
    "derived_flag_column": DERIVED_FLAG_COLUMN,
    "value_tier_high_label": VALUE_TIER_HIGH_LABEL,
    "value_tier_low_label": VALUE_TIER_LOW_LABEL,
    "validation_abs_tolerance": VALIDATION_ABS_TOLERANCE,
    "validation_rel_tolerance": VALIDATION_REL_TOLERANCE,
    "reference_row_count": REFERENCE_ROW_COUNT,
    "reference_column_count": REFERENCE_COLUMN_COUNT,
    "reference_dutiablevaluephp_sum": REFERENCE_DUTIABLEVALUEPHP_SUM,
}