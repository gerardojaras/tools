import csv
import json
from collections import defaultdict

fee_data = defaultdict(lambda: {"count": 0, "sum": 0, "loan_ids": []})

with open(
    "/Users/gerardojaramillo/code/tools/extract-2025-12-31T18_52_40.594Z.csv", "r"
) as file:
    reader = csv.reader(file)
    next(reader)  # skip header
    for row in reader:
        if len(row) >= 4:
            content = row[3]
            json_log = content.split("] ", 1)[1]
            json_log = json_log.replace('""', '"')
            json_log = json_log.strip()
            try:
                log_data = json.loads(json_log)
                event_json_str = log_data["msg"]
                event_data = json.loads(event_json_str)
                data = event_data.get("detail", {}).get("data", {})
                late_fee = data.get("installment_late_fee", 0)
                if late_fee > 0:
                    user_id = data.get("user_id")
                    loan_id = data.get("loan_id")
                    fee_data[user_id]["count"] += 1
                    fee_data[user_id]["sum"] += late_fee
                    fee_data[user_id]["loan_ids"].append(loan_id)
            except json.JSONDecodeError as e:
                print(f"JSON error: {e}")
                continue

print(f"Found {len(fee_data)} unique users with late fees")
for user_id, data in fee_data.items():
    loan_ids_str = ", ".join(data["loan_ids"])
    print(
        f"user_id: {user_id}, loan_ids: {loan_ids_str}, number_of_late_fees: {data['count']}, total_late_fee: {data['sum']}"
    )

# Write to CSV file
output_file = "late_fee_2025-12-31.csv"
with open(output_file, "w", newline="") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(
        ["row_number", "user_id", "loan_ids", "number_of_late_fees", "total_late_fee"]
    )
    row_num = 1
    for user_id, data in fee_data.items():
        loan_ids_str = ", ".join(data["loan_ids"])
        writer.writerow([row_num, user_id, loan_ids_str, data["count"], data["sum"]])
        row_num += 1

print(f"Results written to {output_file}")
