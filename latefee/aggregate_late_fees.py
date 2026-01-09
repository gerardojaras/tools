#!/usr/bin/env python3
import argparse
import csv
from collections import defaultdict
from pathlib import Path


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Aggregate a per-user late-fee CSV into total late fee per user."
    )
    parser.add_argument(
        "--input",
        "-i",
        default="late_fee_2025-12-31.csv",
        help="Input CSV path (e.g. produced by parse_late_fees.py).",
    )
    parser.add_argument(
        "--output",
        "-o",
        default="unique_user_late_fees_2025-12-31.csv",
        help="Output CSV path.",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    input_path = Path(args.input)
    output_path = Path(args.output)

    fee_sums = defaultdict(int)

    with input_path.open("r", newline="") as file:
        reader = csv.DictReader(file)
        for row in reader:
            user_id = row.get("user_id")
            if not user_id:
                continue
            total_fee = row.get("total_late_fee")
            if total_fee is None:
                continue
            fee_sums[user_id] += int(total_fee)

    with output_path.open("w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["user_id", "total_late_fee"])
        for user_id, total_fee in fee_sums.items():
            writer.writerow([user_id, total_fee])

    print(f"Aggregated results written to {output_path}")
    print(f"Unique users: {len(fee_sums)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
