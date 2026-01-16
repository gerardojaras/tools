#!/usr/bin/env python3
import json
from pathlib import Path

infile = Path(__file__).parent / "vana-pay.csv"
out_dir = Path(__file__).parent
batch_size = 120

with infile.open("r", encoding="utf-8") as f:
    lines = [line.strip() for line in f if line.strip()]

batches = [lines[i : i + batch_size] for i in range(0, len(lines), batch_size)]
created = []
for idx, batch in enumerate(batches, start=1):
    fname = out_dir / f"loan_ids_batch_{idx:02d}.json"
    # Wrap in the required structure
    data = {
        "data": {
            "loan_ids": batch
        }
    }
    with fname.open("w", encoding="utf-8") as of:
        json.dump(data, of, indent=2)
    created.append(str(fname.name))

manifest = out_dir / "loan_ids_batches_manifest.json"
with manifest.open("w", encoding="utf-8") as mf:
    json.dump(
        {"batches": created, "total_records": len(lines), "batch_size": batch_size},
        mf,
        indent=2,
    )

print("WROTE", len(created), "batch files; total records =", len(lines))
for c in created:
    print("-", c)
