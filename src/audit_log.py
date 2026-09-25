"""
Audit logging for the Philippine Customs 2015 pipeline.

Provides a small, shared way for each pipeline step (load, filter, group,
etc.) to record what it did, so audit_log.csv reflects the real sequence
of operations as the program runs -- not reconstructed after the fact.
"""

from __future__ import annotations

import pandas as pd


def create_audit_log() -> list[dict]:
    """Create an empty audit log list to be passed through the pipeline."""
    return []


def append_audit_entry(
    log: list[dict],
    step: str,
    operation: str,
    rule: str,
    rows_before,
    rows_after,
) -> list[dict]:
    """
    Append one entry to the audit log.

    Parameters
    ----------
    log: The shared audit log list, built up across pipeline steps.
    step: Short name for the pipeline stage (e.g. "load", "filter", "group").
    operation: What function/operation was performed.
    rule: The rule or condition applied (e.g. the filter condition).
    rows_before: Row count before this step (None if not applicable, e.g.
        at the very first load step).
    rows_after: Row count after this step.

    Returns
    -------
    list[dict]: the same log list, with the new entry appended.
    """
    log.append({
        "step": step,
        "operation": operation,
        "rule": rule,
        "rows_before": rows_before,
        "rows_after": rows_after,
    })
    return log


def write_audit_log(log: list[dict], output_path) -> None:
    """Write the accumulated audit log entries to CSV."""
    df = pd.DataFrame(log)
    df.to_csv(output_path, index=False)