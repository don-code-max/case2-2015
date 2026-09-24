import sys
import config
import pandas as pd


class CustomsProcessor:

    def __init__(self, df: pd.DataFrame, cfg=None) -> None:
        self.raw_df = df
        self.config = cfg if cfg is not None else config
        self.filtered_df: pd.DataFrame | None = None
        self.excluded_df: pd.DataFrame | None = None

    def apply_filter(self) -> pd.DataFrame:
        # missing filter values -> excluded
        missing_mask = (
            self.raw_df[self.config.CATEGORY_COLUMN_2].isna()
            | self.raw_df[self.config.MEASURE_COLUMN].isna()
        )
        self.excluded_df = self.raw_df.loc[missing_mask]
        candidates = self.raw_df.loc[~missing_mask]

        condition1 = (
            candidates[self.config.CATEGORY_COLUMN_2]
            == self.config.FILTER_QUARTER
        )
        condition2 = (
            candidates[self.config.MEASURE_COLUMN]
            > self.config.FILTER_MIN_VALUE
        )

        self.filtered_df = candidates.loc[condition1 & condition2]

        if len(self.filtered_df) == 0:
            print(
                "ERROR: filter returned 0 rows. Check filter conditions in"
                " config.py.",
                file=sys.stderr,
            )
            sys.exit(1)  # Properly indented inside the if-block now

        return self.filtered_df

    def add_derived_columns(self) -> pd.DataFrame:
        df = self.filtered_df.copy()
        df[self.config.DERIVED_NUMERIC_COLUMN] = (
            df[self.config.MEASURE_COLUMN] / self.config.DERIVED_NUMERIC_DIVISOR
        )
        median_value = df[self.config.MEASURE_COLUMN].median()
        df[self.config.DERIVED_FLAG_COLUMN] = df[
            self.config.MEASURE_COLUMN
        ].apply(
            lambda v: (
                self.config.VALUE_TIER_HIGH_LABEL
                if v >= median_value
                else self.config.VALUE_TIER_LOW_LABEL
            )
        )
        self.filtered_df = df
        return df

    def sort(self, by: str = None) -> pd.DataFrame:
        sort_col = by or self.config.MEASURE_COLUMN
        self.filtered_df = self.filtered_df.sort_values(
            sort_col, ascending=False
        )
        return self.filtered_df


def check_numeric_columns(
    df: pd.DataFrame, numeric_columns: list[str]
) -> list[str]:
    problems = []
    for col in numeric_columns:
        if col not in df.columns:
            continue
        if not pd.api.types.is_numeric_dtype(df[col]):
            problems.append(col)
    return problems
