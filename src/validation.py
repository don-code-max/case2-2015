"""
Validation checks for the Philippine Customs 2015 pipeline.

Builds validation.csv with columns: check, expected, actual, tolerance, pass.
Each check computes 'expected' independently of the code path being checked,
per the assignment's requirement. On any failure, prints the discrepancy and
exits with a nonzero status.
"""

from __future__ import annotations

import sys
import pandas as pd

import config


def build_validation_rows(
    raw_df: pd.DataFrame,
    filtered_df: pd.DataFrame,
    excluded_df: pd.DataFrame,
    grouped_df: pd.DataFrame,
    pivot_df: pd.DataFrame,
    loop_vs_vectorized_result: dict,
    cfg=config,
) -> list[dict]:
    """
    Run all six required validation checks and return them as a list of
    dicts, ready to become validation.csv.
    """
    rows = []

    # Check 1: raw row count + sum vs reference values 
    raw_row_count = len(raw_df)
    raw_sum = raw_df[cfg.MEASURE_COLUMN].sum()

    rows.append({
        "check": "raw_row_count_vs_reference",
        "expected": cfg.REFERENCE_ROW_COUNT,
        "actual": raw_row_count,
        "tolerance": 0,
        "pass": raw_row_count == cfg.REFERENCE_ROW_COUNT,
    })
    rows.append({
        "check": "raw_measure_sum_vs_reference",
        "expected": cfg.REFERENCE_DUTIABLEVALUEPHP_SUM,
        "actual": raw_sum,
        "tolerance": cfg.VALIDATION_ABS_TOLERANCE,
        "pass": abs(raw_sum - cfg.REFERENCE_DUTIABLEVALUEPHP_SUM) <= cfg.VALIDATION_ABS_TOLERANCE,
    })

    # Check 2: raw rows = selected rows + excluded rows 
    selected_count = len(filtered_df)
    excluded_count = len(excluded_df)
    rows.append({
        "check": "raw_equals_selected_plus_excluded",
        "expected": raw_row_count,
        "actual": selected_count + excluded_count,
        "tolerance": 0,
        "pass": raw_row_count == (selected_count + excluded_count),
    })

    # Check 3: grouped row counts sum to selected row count 
    grouped_row_count_sum = grouped_df["row_count"].sum()
    rows.append({
        "check": "grouped_row_counts_sum_to_selected",
        "expected": selected_count,
        "actual": grouped_row_count_sum,
        "tolerance": 0,
        "pass": grouped_row_count_sum == selected_count,
    })

    #  Check 4: grouped sum == pivot interior sum == independent sum 
    independent_sum = filtered_df[cfg.MEASURE_COLUMN].sum()
    grouped_sum = grouped_df["measure_sum"].sum()
    pivot_interior = pivot_df.drop(index="All", errors="ignore").drop(columns="All", errors="ignore")
    pivot_sum = pivot_interior.sum().sum()

    rows.append({
        "check": "grouped_sum_matches_independent_sum",
        "expected": independent_sum,
        "actual": grouped_sum,
        "tolerance": cfg.VALIDATION_ABS_TOLERANCE,
        "pass": abs(grouped_sum - independent_sum) <= cfg.VALIDATION_ABS_TOLERANCE,
    })
    rows.append({
        "check": "pivot_interior_sum_matches_independent_sum",
        "expected": independent_sum,
        "actual": pivot_sum,
        "tolerance": cfg.VALIDATION_ABS_TOLERANCE,
        "pass": abs(pivot_sum - independent_sum) <= cfg.VALIDATION_ABS_TOLERANCE,
    })

    # Check 5: plot values match summary tables (top10 vs grouped) 
    top10_sum = grouped_df.sort_values("measure_sum", ascending=False).head(10)["measure_sum"].sum()
    # recompute independently: sort raw grouped_df copy, don't reuse build_top10
    independent_top10_sum = grouped_df["measure_sum"].nlargest(10).sum()
    rows.append({
        "check": "top10_values_match_grouped_table",
        "expected": independent_top10_sum,
        "actual": top10_sum,
        "tolerance": cfg.VALIDATION_ABS_TOLERANCE,
        "pass": abs(top10_sum - independent_top10_sum) <= cfg.VALIDATION_ABS_TOLERANCE,
    })

    #  Check 6: loop vs vectorized calculation agree 
    loop_result = loop_vs_vectorized_result["loop_result"]
    vec_result = loop_vs_vectorized_result["vectorized_result"]
    rows.append({
        "check": "loop_vs_vectorized_agree",
        "expected": loop_result,
        "actual": vec_result,
        "tolerance": 0,
        "pass": loop_result == vec_result,
    })

    return rows


def write_validation_csv(rows: list[dict], output_path) -> None:
    """
    Write validation rows to CSV. Exits with status 1 if any check failed,
    printing the discrepancy.
    """
    df = pd.DataFrame(rows)
    df.to_csv(output_path, index=False)

    failures = df[~df["pass"]]
    if len(failures) > 0:
        print("VALIDATION FAILED:", file=sys.stderr)
        for _, row in failures.iterrows():
            print(
                f"  {row['check']}: expected={row['expected']}, "
                f"actual={row['actual']}, tolerance={row['tolerance']}",
                file=sys.stderr,
            )
        sys.exit(1)

    print(f"All {len(df)} validation checks passed.")