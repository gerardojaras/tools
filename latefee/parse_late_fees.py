#!/usr/bin/env python3
import argparse
import csv
import json
from collections import defaultdict
from pathlib import Path


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Parse a CSV export containing JSON logs, extract late-fee events, "
            "and write a per-user CSV summary."
        )
    )
    parser.add_argument(
        "--input",
        "-i",
        default="/Users/gerardojaramillo/code/tools/extract-2025-12-31T18_52_40.594Z.csv",
        help="Path to the CSV export to parse.",
    )
    parser.add_argument(
        "--output",
        "-o",
        default="late_fee_2025-12-31.csv",
        help="Output CSV path to write.",
    )
    parser.add_argument(
        "--json-column",
        type=int,
        default=3,
        help="0-based index of the CSV column that contains the JSON log string.",
    )
    parser.add_argument(
        "--quiet",
        action="store_true",
        help="Do not print per-user summary lines.",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    input_path = Path(args.input)
    output_path = Path(args.output)

    fee_data = defaultdict(lambda: {"count": 0, "sum": 0, "loan_ids": []})

    with input_path.open("r", newline="") as file:
        reader = csv.reader(file)
        next(reader, None)  # skip header
        for row in reader:
            if len(row) <= args.json_column:
                continue

            content = row[args.json_column]
            if "] " not in content:
                continue

            json_log = content.split("] ", 1)[1]
            json_log = json_log.replace('""', '"').strip()
            try:
                log_data = json.loads(json_log)
                event_json_str = log_data.get("msg")
                if not isinstance(event_json_str, str):
                    continue

                event_data = json.loads(event_json_str)
                data = event_data.get("detail", {}).get("data", {})
                late_fee = data.get("installment_late_fee", 0)
                if late_fee and late_fee > 0:
                    user_id = data.get("user_id")
                    loan_id = data.get("loan_id")
                    if not user_id:
                        continue
                    fee_data[user_id]["count"] += 1
                    fee_data[user_id]["sum"] += late_fee
                    if loan_id:
                        fee_data[user_id]["loan_ids"].append(loan_id)
            except json.JSONDecodeError as e:
                print(f"JSON error: {e}")
                continue

    print(f"Found {len(fee_data)} unique users with late fees")
    if not args.quiet:
        for user_id, data in fee_data.items():
            loan_ids_str = ", ".join(data["loan_ids"])
            print(
                f"user_id: {user_id}, loan_ids: {loan_ids_str}, number_of_late_fees: {data['count']}, total_late_fee: {data['sum']}"
            )

    with output_path.open("w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(
            [
                "user_id",
                "loan_ids",
                "number_of_late_fees",
                "total_late_fee",
            ]
        )
        for user_id, data in fee_data.items():
            writer.writerow(
                [
                    user_id,
                    ", ".join(data["loan_ids"]),
                    data["count"],
                    data["sum"],
                ]
            )

    print(f"Results written to {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
