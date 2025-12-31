#!/usr/bin/env python3
import json
from pathlib import Path
from datetime import date

p = Path(__file__).parent
date_str = date.today().isoformat()  # YYYY-MM-DD

# Find batch files
batch_files = sorted(p.glob("customerIds_batch_*.json"))
# Exclude manifest
batch_files = [f for f in batch_files if f.name != "customerIds_batches_manifest.json"]
if not batch_files:
    print("No batch files found to rename.")
    raise SystemExit(1)

renamed = []
for f in batch_files:
    new_name = f"{f.stem}_{date_str}.json"
    new_path = p / new_name
    # If target exists, overwrite
    if new_path.exists():
        new_path.unlink()
    f.rename(new_path)
    renamed.append(new_name)

# Update manifest if present
manifest_path = p / "customerIds_batches_manifest.json"
if manifest_path.exists():
    with manifest_path.open("r", encoding="utf-8") as mf:
        manifest = json.load(mf)
    manifest["batches"] = renamed
    with manifest_path.open("w", encoding="utf-8") as mf:
        json.dump(manifest, mf, indent=2)

print("Renamed", len(renamed), "files:")
for n in renamed:
    print("-", n)
print("Updated manifest:", manifest_path.name if manifest_path.exists() else "none")
