#!/usr/bin/env python3
"""Small CLI to run the scripts in this repo.

Goal: a single entrypoint you can extend by adding new subcommands.

Examples:
  python tools_cli.py list
  python tools_cli.py latefee parse -i export.csv -o late_fee.csv
  python tools_cli.py latefee aggregate -i late_fee.csv -o totals.csv
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).parent


def _python() -> str:
    return sys.executable or "python3"


def _run_script(script: Path, extra_args: list[str]) -> int:
    if not script.exists():
        raise SystemExit(f"Script not found: {script}")
    cmd = [_python(), str(script), *extra_args]
    return subprocess.call(cmd)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Tools launcher")
    sub = parser.add_subparsers(dest="cmd", required=True)

    sub.add_parser("list", help="List available tool commands")

    latefee = sub.add_parser("latefee", help="Late-fee related tools")
    latefee_sub = latefee.add_subparsers(dest="latefee_cmd", required=True)

    lf_parse = latefee_sub.add_parser("parse", help="Parse log export -> late_fee CSV")
    lf_parse.add_argument("args", nargs=argparse.REMAINDER, help="Args passed to script")

    lf_agg = latefee_sub.add_parser("aggregate", help="Aggregate late_fee CSV -> totals")
    lf_agg.add_argument("args", nargs=argparse.REMAINDER, help="Args passed to script")

    lf_extract = latefee_sub.add_parser(
        "extract-user-ids", help="Extract user_id/loan_id pairs from report"
    )
    lf_extract.add_argument("args", nargs=argparse.REMAINDER, help="Args passed to script")

    customer = sub.add_parser("customerids", help="Customer ID batching tools")
    customer_sub = customer.add_subparsers(dest="customer_cmd", required=True)

    c_csv = customer_sub.add_parser("from-csv", help="customerIds.csv -> customerIds_batch_*.json")
    c_csv.add_argument("args", nargs=argparse.REMAINDER)

    c_snap = customer_sub.add_parser("from-snapshot", help="snapshot -> customerIds_batch_*.json")
    c_snap.add_argument("args", nargs=argparse.REMAINDER)

    c_wrap = customer_sub.add_parser("wrap-data", help="Wrap batches into {data: ...}")
    c_wrap.add_argument("args", nargs=argparse.REMAINDER)

    c_loan = customer_sub.add_parser("convert-loan-ids", help="Convert to {data:{loan_ids:[...]}}")
    c_loan.add_argument("args", nargs=argparse.REMAINDER)

    c_rename = customer_sub.add_parser("rename-add-date", help="Rename batch files and update manifest")
    c_rename.add_argument("args", nargs=argparse.REMAINDER)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.cmd == "list":
        print("Available commands:")
        print("  latefee parse")
        print("  latefee aggregate")
        print("  latefee extract-user-ids")
        print("  customerids from-csv")
        print("  customerids from-snapshot")
        print("  customerids wrap-data")
        print("  customerids convert-loan-ids")
        print("  customerids rename-add-date")
        return 0

    if args.cmd == "latefee":
        if args.latefee_cmd == "parse":
            return _run_script(REPO_ROOT / "latefee" / "parse_late_fees.py", args.args)
        if args.latefee_cmd == "aggregate":
            return _run_script(REPO_ROOT / "latefee" / "aggregate_late_fees.py", args.args)
        if args.latefee_cmd == "extract-user-ids":
            return _run_script(REPO_ROOT / "latefee" / "extract_user_ids.py", args.args)

    if args.cmd == "customerids":
        if args.customer_cmd == "from-csv":
            return _run_script(REPO_ROOT / "csv_to_json_batches.py", args.args)
        if args.customer_cmd == "from-snapshot":
            return _run_script(REPO_ROOT / "generate_json_batches_from_snapshot.py", args.args)
        if args.customer_cmd == "wrap-data":
            return _run_script(REPO_ROOT / "wrap_batches_in_data.py", args.args)
        if args.customer_cmd == "convert-loan-ids":
            return _run_script(REPO_ROOT / "convert_to_loan_ids.py", args.args)
        if args.customer_cmd == "rename-add-date":
            return _run_script(REPO_ROOT / "rename_batches_add_date.py", args.args)

    parser.error("Unhandled command")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
