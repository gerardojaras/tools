# Late fee tools

This folder groups scripts related to extracting and aggregating late fee information from CSV/log exports.

## Scripts

- `parse_late_fees.py`: Parses a CSV export containing JSON logs, extracts late-fee events, and writes `late_fee_2025-12-31.csv`.
- `aggregate_late_fees.py`: Aggregates the per-event CSV into a per-user total CSV.
- `extract_user_ids.py`: Extracts `(user_id, loan_id)` pairs from a report and writes a `unique_user_ids.csv`.

## Notes

Some scripts currently use absolute input/output paths that may need adjusting per machine.
