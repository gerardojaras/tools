import csv
from collections import defaultdict

# Read the late_fee CSV and aggregate by user_id
fee_sums = defaultdict(int)

with open("late_fee_2025-12-31.csv", "r") as file:
    reader = csv.reader(file)
    next(reader)  # skip header
    for row in reader:
        user_id = row[0]
        late_fee = int(row[2])
        fee_sums[user_id] += late_fee

# Write the aggregated results to a new CSV
output_file = "unique_user_late_fees_2025-12-31.csv"
with open(output_file, "w", newline="") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["user_id", "total_late_fee"])
    for user_id, total_fee in fee_sums.items():
        writer.writerow([user_id, total_fee])

print(f"Aggregated results written to {output_file}")
print(f"Unique users: {len(fee_sums)}")
for user_id, total_fee in fee_sums.items():
    print(f"user_id: {user_id}, total_late_fee: {total_fee}")
