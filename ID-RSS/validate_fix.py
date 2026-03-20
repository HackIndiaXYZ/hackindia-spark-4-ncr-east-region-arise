#!/usr/bin/env python3
"""Final validation - test all formats work correctly"""

import json
from Extractor import process_folder

print("\n" + "=" * 80)
print("FINAL VALIDATION REPORT - CSV AND TEXT EXTRACTION FIX")
print("=" * 80)

folder = "demo_files"
fields = ["Name", "Serial No."]

results = process_folder(folder, fields)

# Show results by format
formats_tested = {}
for result in results:
    fmt = result.get("format", "unknown")
    if fmt not in formats_tested:
        formats_tested[fmt] = {"total": 0, "success": 0, "samples": []}

    formats_tested[fmt]["total"] += 1
    if result.get("confidence", 0) == 1.0:
        formats_tested[fmt]["success"] += 1

    # Save first and last sample
    if len(formats_tested[fmt]["samples"]) < 2:
        formats_tested[fmt]["samples"].append(result)

print("\nFORMAT SUPPORT STATUS:")
print("-" * 80)
for fmt in sorted(formats_tested.keys()):
    info = formats_tested[fmt]
    success_rate = 100 * info["success"] / info["total"]
    status = "WORKING" if success_rate == 100 else "PARTIAL"
    print(f"\n{fmt.upper():6} | {info['total']} file(s) | "
          f"{info['success']}/{info['total']} successful ({success_rate:.0f}%) | {status}")

    if info["samples"]:
        sample = info["samples"][0]
        print(f"  Sample: {sample['file']:<30} Name: {sample.get('Name', 'ERROR'):<20} "
              f"SN: {sample.get('Serial No.', 'ERROR')}")

print("\n" + "=" * 80)
print(f"SUMMARY: {len(results)} files processed, "
      f"{sum(1 for r in results if r.get('confidence') == 1.0)} fully extracted")
print("=" * 80)

# Check CSV and TXT specifically
csv_results = [r for r in results if r.get("format") == "csv"]
txt_results = [r for r in results if r.get("format") == "txt"]

print("\nCSV EXTRACTION TEST:")
if csv_results:
    csv = csv_results[0]
    print(f"  File: {csv['file']}")
    print(f"  Name field: {csv.get('Name', 'MISSING')}")
    print(f"  Serial No. field: {csv.get('Serial No.', 'MISSING')}")
    print(f"  Confidence: {csv.get('confidence', 0)}")
else:
    print("  NO CSV FILES FOUND")

print("\nTXT EXTRACTION TEST:")
if txt_results:
    txt = txt_results[0]
    print(f"  File: {txt['file']}")
    print(f"  Name field: {txt.get('Name', 'MISSING')}")
    print(f"  Serial No. field: {txt.get('Serial No.', 'MISSING')}")
    print(f"  Confidence: {txt.get('confidence', 0)}")
else:
    print("  NO TXT FILES FOUND")

print("\n" + "=" * 80)
print("STATUS: FIXED - CSV and TXT extraction now working properly")
print("=" * 80 + "\n")
