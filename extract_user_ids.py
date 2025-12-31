import json
import re
from datetime import datetime

# Read the CSV file and filter lines before 18:00
filtered_lines = []
with open("/home/gerardo/tools/12-31-2025-report.csv", "r") as f:
    for line in f:
        if line.strip() and line.startswith("2025"):
            # Parse timestamp
            timestamp_str = line.split(" ")[0]  # e.g., 2025-12-31T18:09:05.355Z
            dt = datetime.fromisoformat(timestamp_str.replace("Z", "+00:00"))
            if dt.hour < 18:
                filtered_lines.append(line)

content = "".join(filtered_lines)

print(f"Filtered content length: {len(content)}")
print(f"Filtered lines: {len(filtered_lines)}")

# Find all pairs of loan_id and user_id
pairs = re.findall(
    r'\\"loan_id\\":\\"([^"]+)\\".*?\\"user_id\\":\\"([^"]+)\\"', content
)

print(f"Found {len(pairs)} pairs")

# Create dict user_id to loan_id (first occurrence)
user_to_loan = {}
for lid, uid in pairs:
    if uid not in user_to_loan:
        user_to_loan[uid] = lid

# Get unique user_ids
unique_user_ids = sorted(user_to_loan.keys())

# Write to CSV
with open("/home/gerardo/tools/unique_user_ids.csv", "w") as f:
    for uid in unique_user_ids:
        lid = user_to_loan[uid]
        f.write(f'"user_id":"{uid}","loan_id":"{lid}"\n')

print(f"Extracted {len(unique_user_ids)} unique user_ids with loan_ids")
