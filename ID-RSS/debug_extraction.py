#!/usr/bin/env python3
"""Debug script to test CSV and TXT extraction"""

from Extractor import (
    extract_from_csv,
    extract_from_txt,
    extract_from_docx,
    extract_field,
    process_folder
)
import json

print("=" * 60)
print("DEBUGGING CSV AND TXT EXTRACTION")
print("=" * 60)

# Test fields
fields = ["Name", "Serial No.", "Department"]

print("\n1. Testing CSV extraction:")
print("-" * 60)
csv_result = extract_from_csv("demo_files/sample_data.csv", fields)
print(json.dumps(csv_result, indent=2))

print("\n2. Testing TXT extraction:")
print("-" * 60)
txt_result = extract_from_txt("demo_files/student_record.txt", fields)
print(json.dumps(txt_result, indent=2))

print("\n3. Manual field extraction from CSV:")
print("-" * 60)
with open("demo_files/sample_data.csv", 'r', encoding='utf-8') as f:
    import csv
    reader = csv.reader(f)
    csv_text = ""
    for row in reader:
        csv_text += " | ".join(row) + "\n"

print("Joined CSV text:")
print(repr(csv_text))
print("\nTrying to extract 'Name':")
name_value = extract_field(csv_text, "Name")
print(f"Result: '{name_value}'")

print("\n4. Manual field extraction from TXT:")
print("-" * 60)
with open("demo_files/student_record.txt", 'r', encoding='utf-8') as f:
    txt_text = f.read()

print("Raw TXT content:")
print(repr(txt_text))
print("\nTrying to extract 'Name':")
name_value = extract_field(txt_text, "Name")
print(f"Result: '{name_value}'")

print("\n5. Testing process_folder with all formats:")
print("-" * 60)
results = process_folder("demo_files", fields)
print(f"Total files processed: {len(results)}")
for r in results[-5:]:  # Show last 5 files
    print(f"{r['file']:<30} Format: {r.get('format', 'N/A'):<6} Confidence: {r.get('confidence', 0)}")
    if "error" in r:
        print(f"  ERROR: {r['error']}")

print("\n" + "=" * 60)
print("DEBUG COMPLETE")
print("=" * 60)
