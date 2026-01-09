#!/usr/bin/env python3
import argparse
import re
from datetime import datetime
from pathlib import Path


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Extract (user_id, loan_id) pairs from a report file containing escaped JSON."
        )
    )
    parser.add_argument(
        "--input",
        "-i",
        default="/home/gerardo/tools/12-31-2025-report.csv",
        help="Input report path.",
    )
    parser.add_argument(
        "--output",
        "-o",
        default="/home/gerardo/tools/unique_user_ids.csv",
        help="Output CSV-like file path.",
    )
    parser.add_argument(
        "--before-hour",
        type=int,
        default=18,
        help="Only include lines with timestamps before this hour (0-23).",
    )
    parser.add_argument(
        "--line-prefix",
        default="2025",
        help="Only include lines starting with this prefix (default: 2025).",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    input_path = Path(args.input)
    output_path = Path(args.output)

    filtered_lines: list[str] = []
    with input_path.open("r", encoding="utf-8") as f:
        for line in f:
            if line.strip() and line.startswith(args.line_prefix):
                timestamp_str = line.split(" ")[0]
                dt = datetime.fromisoformat(timestamp_str.replace("Z", "+00:00"))
                if dt.hour < args.before_hour:
                    filtered_lines.append(line)

    content = "".join(filtered_lines)
    print(f"Filtered content length: {len(content)}")
    print(f"Filtered lines: {len(filtered_lines)}")

    pairs = re.findall(
        r'\\"loan_id\\":\\"([^\"]+)\\".*?\\"user_id\\":\\"([^\"]+)\\"',
        content,
    )
    print(f"Found {len(pairs)} pairs")

    user_to_loan: dict[str, str] = {}
    for loan_id, user_id in pairs:
        if user_id not in user_to_loan:
            user_to_loan[user_id] = loan_id

    unique_user_ids = sorted(user_to_loan.keys())
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8") as f:
        for user_id in unique_user_ids:
            f.write(f'"user_id":"{user_id}","loan_id":"{user_to_loan[user_id]}"\n')

    print(f"Extracted {len(unique_user_ids)} unique user_ids with loan_ids")
    print(f"Wrote {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
