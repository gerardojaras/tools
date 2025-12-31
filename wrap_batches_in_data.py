#!/usr/bin/env python3
import json
from pathlib import Path

p = Path(__file__).parent
files = sorted(p.glob("customerIds_batch_*.json"))
updated = []
for f in files:
    try:
        with f.open("r", encoding="utf-8") as fh:
            content = json.load(fh)
    except Exception as e:
        print("SKIP", f.name, "read error:", e)
        continue
    # If already wrapped, skip
    if (
        isinstance(content, dict)
        and "data" in content
        and isinstance(content["data"], list)
    ):
        continue
    new = {"data": content}
    with f.open("w", encoding="utf-8") as fh:
        json.dump(new, fh, indent=2)
    updated.append(f.name)

print("Updated", len(updated), "files")
for n in updated:
    print("-", n)
