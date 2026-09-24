# Task Ownership

- Person A: loader.py, config.py, validation.csv logic
- Person B: processing.py (filtering/transforms + required class)
- Person C: aggregation.py (grouped/pivot/top10 outputs)
- Person D: plotting.py, NumPy timing comparison, README/contributions.md

Everyone: audit_log.csv from their own step, review a teammate's PR before merge.
