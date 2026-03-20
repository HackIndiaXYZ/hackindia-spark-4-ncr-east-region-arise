#!/usr/bin/env python3
"""Show extraction results grouped by file format"""

import json
from Extractor import process_folder
from collections import defaultdict

folder = "demo_files"
fields = ["Name", "Serial No."]

results = process_folder(folder, fields)

# Group results by format
by_format = defaultdict(list)
for result in results:
    fmt = result.get("format", "unknown")
    by_format[fmt].append(result)

print("\n" + "=" * 70)
print("EXTRACTION RESULTS BY FILE FORMAT")
print("=" * 70)

for fmt in sorted(by_format.keys()):
    files = by_format[fmt]
    perfect = sum(1 for f in files if f.get("confidence", 0) == 1.0)
    print(f"\n[{fmt.upper()}] {len(files)} file(s) - {perfect}/{len(files)} with 100% confidence")
    print("-" * 70)

    for f in files:
        status = "[OK]" if f.get("confidence", 0) == 1.0 else "[FAIL]"
        print(f"{status} {f['file']:<30} Name: {f.get('Name', '—'):<25} SN: {f.get('Serial No.', '—')}")
        if "error" in f:
            print(f"  ERROR: {f['error']}")

print("\n" + "=" * 70)
total_perfect = sum(1 for r in results if r.get("confidence", 0) == 1.0)
print(f"SUMMARY: {total_perfect}/{len(results)} files fully extracted")
print("=" * 70 + "\n")
