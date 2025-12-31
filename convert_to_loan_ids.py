#!/usr/bin/env python3
import json
from pathlib import Path

p = Path(__file__).parent
files = sorted(p.glob("customerIds_batch_*.json"))
updated = []
for f in files:
    if f.name == "customerIds_batches_manifest.json":
        continue
    try:
        with f.open("r", encoding="utf-8") as fh:
            content = json.load(fh)
    except Exception as e:
        print("SKIP", f.name, "read error:", e)
        continue
    # If content is dict with data as list, wrap into loan_ids
    if isinstance(content, dict):
        data_val = content.get("data")
        if isinstance(data_val, list):
            new = {"data": {"loan_ids": data_val}}
        elif (
            isinstance(data_val, dict)
            and "loan_ids" in data_val
            and isinstance(data_val["loan_ids"], list)
        ):
            # already in desired shape
            continue
        else:
            # unknown shape — skip
            print("SKIP", f.name, "unknown `data` shape")
            continue
    else:
        # if the file is a raw list, wrap accordingly
        if isinstance(content, list):
            new = {"data": {"loan_ids": content}}
        else:
            print("SKIP", f.name, "unknown root shape")
            continue
    with f.open("w", encoding="utf-8") as fh:
        json.dump(new, fh, indent=2)
    updated.append(f.name)

print("Updated", len(updated), "files")
for n in updated:
    print("-", n)
