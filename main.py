"""
Main entry point for the Philippine Customs 2015 data summary program.

Run with: python main.py

Chains together: load -> validate columns -> filter -> derive columns ->
sort -> group/pivot/top10 -> plot -> validate -> audit log. Writes all
required output files into config.OUTPUT_DIR.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "src"))

import config
from loader import load_data, validate_required_columns, inspect_data
from processing import CustomsProcessor
from aggregation import build_grouped, build_grouped_two, build_pivot, build_top10
from plotting import plot_bar, plot_heatmap, compare_loop_vs_vectorized
from validation import build_validation_rows, write_validation_csv
from audit_log import create_audit_log, append_audit_entry, write_audit_log


def main() -> None:
    """Run the full pipeline end-to-end."""
    config.OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    log = create_audit_log()

    # --- Load ---
    print("Loading data...")
    raw_df = load_data()
    append_audit_entry(
        log, step="load", operation="load_data",
        rule="read CSV from config.INPUT_PATH",
        rows_before=None, rows_after=len(raw_df),
    )

    validate_required_columns(raw_df)
    append_audit_entry(
        log, step="validate_columns", operation="validate_required_columns",
        rule="check required columns present",
        rows_before=len(raw_df), rows_after=len(raw_df),
    )

    # --- Inspect (row counts, dtypes, missing values) ---
    print("\nInspecting raw data...")
    inspect_data(raw_df)

    # --- Filter, derive, sort ---
    print("\nFiltering and transforming...")
    proc = CustomsProcessor(raw_df)
    filtered = proc.apply_filter()
    append_audit_entry(
        log, step="filter", operation="apply_filter",
        rule=f"{config.CATEGORY_COLUMN_2} == '{config.FILTER_QUARTER}' AND "
             f"{config.MEASURE_COLUMN} > {config.FILTER_MIN_VALUE}",
        rows_before=len(raw_df), rows_after=len(filtered),
    )
    append_audit_entry(
        log, step="exclude", operation="apply_filter (excluded branch)",
        rule="missing filter value OR filter condition not met",
        rows_before=len(raw_df), rows_after=len(proc.excluded_df),
    )

    filtered = proc.add_derived_columns()
    append_audit_entry(
        log, step="derive_columns", operation="add_derived_columns",
        rule=f"add {config.DERIVED_NUMERIC_COLUMN} and {config.DERIVED_FLAG_COLUMN}",
        rows_before=len(filtered), rows_after=len(filtered),
    )

    filtered = proc.sort()
    append_audit_entry(
        log, step="sort", operation="sort",
        rule=f"sort by {config.MEASURE_COLUMN} descending",
        rows_before=len(filtered), rows_after=len(filtered),
    )

    # --- Aggregate ---
    print("\nBuilding summary tables...")
    grouped = build_grouped(filtered)
    grouped.to_csv(config.OUTPUT_DIR / "grouped.csv", index=False)
    append_audit_entry(
        log, step="group", operation="build_grouped",
        rule=f"group by {config.CATEGORY_COLUMN_1}",
        rows_before=len(filtered), rows_after=len(grouped),
    )

    grouped_two = build_grouped_two(filtered)
    grouped_two.to_csv(config.OUTPUT_DIR / "grouped_two.csv", index=False)
    append_audit_entry(
        log, step="group_two", operation="build_grouped_two",
        rule=f"group by {config.CATEGORY_COLUMN_1} and {config.CATEGORY_COLUMN_2}",
        rows_before=len(filtered), rows_after=len(grouped_two),
    )

    pivot = build_pivot(filtered)
    pivot.to_csv(config.OUTPUT_DIR / "pivot.csv")
    append_audit_entry(
        log, step="pivot", operation="build_pivot",
        rule="pivot_table with margins",
        rows_before=len(filtered), rows_after=len(pivot),
    )

    top10 = build_top10(grouped)
    top10.to_csv(config.OUTPUT_DIR / "top10.csv", index=False)
    append_audit_entry(
        log, step="top10", operation="build_top10",
        rule="top 10 groups by measure_sum",
        rows_before=len(grouped), rows_after=len(top10),
    )

    # --- Plot ---
    print("\nGenerating plots...")
    plot_bar(top10, config.OUTPUT_DIR / "bar.png", config)
    plot_heatmap(pivot, config.OUTPUT_DIR / "heatmap.png")

    # --- NumPy loop vs vectorized comparison ---
    print("\nRunning loop vs vectorized comparison...")
    loop_result = compare_loop_vs_vectorized(
        filtered[config.MEASURE_COLUMN].values, threshold=1_000_000
    )
    print(f"  Loop result: {loop_result['loop_result']}, "
          f"Vectorized result: {loop_result['vectorized_result']}")
    print(f"  Median loop time: {loop_result['median_loop_time_sec']:.6f}s, "
          f"Median vectorized time: {loop_result['median_vectorized_time_sec']:.6f}s")

    # --- Validate ---
    print("\nRunning validation checks...")
    validation_rows = build_validation_rows(
        raw_df=raw_df,
        filtered_df=filtered,
        excluded_df=proc.excluded_df,
        grouped_df=grouped,
        pivot_df=pivot,
        loop_vs_vectorized_result=loop_result,
    )
    write_validation_csv(validation_rows, config.OUTPUT_DIR / "validation.csv")

    # --- Write audit log ---
    write_audit_log(log, config.OUTPUT_DIR / "audit_log.csv")

    print(f"\nDone. All outputs written to {config.OUTPUT_DIR}/")


if __name__ == "__main__":
    main()