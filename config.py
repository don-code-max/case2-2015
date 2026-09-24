"""Configuration for the Philippine Customs 2015 data summary program."""

from pathlib import Path

INPUT_PATH: Path = Path("data/2015.csv")
OUTPUT_DIR: Path = Path("outputs")
CSV_ENCODING: str = "latin1"

REQUIRED_COLUMNS: set[str] = {
    "tq",
    "countryorigin_iso3",
    "dutiablevaluephp",
}

FILTER_QUARTER: str = "2015q4"
FILTER_MIN_VALUE: float = 0.0

CATEGORY_COLUMN_1: str = "countryorigin_iso3"
CATEGORY_COLUMN_2: str = "tq"
MEASURE_COLUMN: str = "dutiablevaluephp"

DERIVED_NUMERIC_COLUMN: str = "dutiablevaluephp_million"
DERIVED_NUMERIC_DIVISOR: float = 1_000_000.0

DERIVED_FLAG_COLUMN: str = "value_tier"
VALUE_TIER_HIGH_LABEL: str = "high"
VALUE_TIER_LOW_LABEL: str = "low"

VALIDATION_ABS_TOLERANCE: float = 1.0
VALIDATION_REL_TOLERANCE: float = 0.0

REFERENCE_ROW_COUNT: int = 2_236_612
REFERENCE_COLUMN_COUNT: int = 30
REFERENCE_DUTIABLEVALUEPHP_SUM: float = 3_587_267_375_257.0

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