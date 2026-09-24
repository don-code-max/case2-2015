import pandas as pd
import config


def build_grouped(df: pd.DataFrame, cfg=config) -> pd.DataFrame:
    """Group by category 1, showing row count, valid measure count, sum, mean."""
    grouped = (
        df.groupby(cfg.CATEGORY_COLUMN_1, dropna=False)
        .agg(
            row_count=(cfg.MEASURE_COLUMN, 'size'),
            valid_measure_count=(cfg.MEASURE_COLUMN, 'count'),
            measure_sum=(cfg.MEASURE_COLUMN, 'sum'),
            measure_mean=(cfg.MEASURE_COLUMN, 'mean'),
        )
        .reset_index()
    )
    return grouped


def build_grouped_two(df: pd.DataFrame, cfg=config) -> pd.DataFrame:
    """Group by both categories, showing row count and measure sum."""
    grouped = (
        df.groupby(
            [cfg.CATEGORY_COLUMN_1, cfg.CATEGORY_COLUMN_2], dropna=False
        )
        .agg(
            row_count=(cfg.MEASURE_COLUMN, 'size'),
            measure_sum=(cfg.MEASURE_COLUMN, 'sum'),
        )
        .reset_index()
    )
    return grouped


def build_pivot(df: pd.DataFrame, cfg=config) -> pd.DataFrame:
    """Pivot table of measure sum across both categories, with margins."""
    pivot = pd.pivot_table(
        df,
        values=cfg.MEASURE_COLUMN,
        index=cfg.CATEGORY_COLUMN_1,
        columns=cfg.CATEGORY_COLUMN_2,
        aggfunc='sum',
        margins=True,
        dropna=False,
    )
    return pivot


def build_top10(grouped_df: pd.DataFrame, cfg=config) -> pd.DataFrame:
    """Top 10 groups by measure sum from grouped.csv (or all, if fewer than 10)."""
    return grouped_df.sort_values('measure_sum', ascending=False).head(10)