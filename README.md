# ID-RSS — Intelligent Document Retrieval & Structuring System

[![Live Site](https://img.shields.io/badge/🌐%20Live%20Site-ID--RSS-1D9E75?style=for-the-badge)](https://ayushh-sharmaa.github.io/ARISE/) [![PPT](https://onedrive.live.com/edit?cid=cc1a3d34e76d2b04&id=CC1A3D34E76D2B04!s88384481f2fe44758a64580fbd32cf99&resid=CC1A3D34E76D2B04!s88384481f2fe44758a64580fbd32cf99&ithint=file%2Cpptx&embed=1&em=2&amp=&wdAr=1.7777777777777777&migratedtospo=true&redeem=aHR0cHM6Ly8xZHJ2Lm1zL3AvYy9jYzFhM2QzNGU3NmQyYjA0L0lRU0JSRGlJX3ZKMVJJcGtXQS05TXMtWkFYN05sb2N3MWJRdlVHSk55Qlg0akw0P2VtPTImYW1wO3dkQXI9MS43Nzc3Nzc3Nzc3Nzc3Nzc3&wdo=2)

## 🎯 Problem Statement
Organizations handle hundreds of student/employee documents (DOCX files) containing structured data scattered across paragraphs. Manual data extraction is slow, error-prone, and doesn't scale. **ID-RSS** automates this.

## ✨ What It Does
- **Batch Processing**: Extract data from 100s of DOCX files in seconds
- **Flexible Field Extraction**: Define which fields to extract (Name, ID, Serial No., etc.)
- **Confidence Scoring**: Tracks extraction quality; shows "—" when data is missing/malformed
- **Professional Excel Export**: Styled spreadsheets with summaries, auto-width columns, color-coded headers
- **Graceful Degradation**: Handles corrupted/unexpected document formats without crashing
- **Web UI**: Simple Flask interface for non-technical users

## 🚀 Quick Start

### Requirements
```bash
Python 3.8+
pip install flask python-docx openpyxl
```

### Run the Server
```bash
cd ID-RSS
python App.py
# Open http://localhost:5000 in browser
```

### Web Interface
1. Enter folder path containing .docx files
2. Specify field names to extract (e.g., "Name", "Serial No.")
3. Click Extract
4. Download Excel report with structured data

### Command Line (Direct Testing)
```bash
# Test extraction
python Extractor.py

# Test export
python Exporter.py
```

## 📊 How It Works

### 1. **Document Extraction** (`Extractor.py`)
- Parses .docx files using `python-docx`
- Uses regex pattern matching: `"FieldName - Value"` format
- Returns dict with extracted fields + confidence score
- **Gracefully handles missing/unexpected formats** (returns "—")

### 2. **Data Export** (`Exporter.py`)
- Converts extracted records to styled Excel (.xlsx)
- Sheet 1: Data table with alternating row colors, frozen headers
- Sheet 2: Summary metadata (processing date, field count, etc.)
- Auto-adjusts column widths

### 3. **Web Server** (`App.py`)
- Flask REST API
- `POST /extract` — Process folder and return extracted data
- `GET /export` — Download Excel file
- Serves responsive HTML UI with dark mode support

## 📈 Performance
- **30 files**: Extract + Export in <5 seconds
- **Scaling**: Linear with document count
- **Memory**: Efficient streaming (no full-file buffering)

## 🎨 Features Demonstrated

### ✅ Working Extraction
Most documents follow the expected format and extract **100% of fields** (confidence = 1.0)  
Example: `student_0002.docx` → Name: "Rahul Verma", Serial No.: "STU-2024-0002"

### ⚠️ Intentional Test Cases (Showcase Robustness)
Some files (`student_0001, 0004, 0009, 0021, 0024`) are intentionally formatted differently to demonstrate:
- How the system handles unexpected document structures
- Confidence scoring when data is missing
- Graceful error handling (shows "—" instead of crashing)
- Real-world resilience

This shows **production-grade error handling** vs. naive extraction that would break on variant formats.

## 📁 Project Structure
```
ID-RSS/
├── App.py                 # Flask server
├── Extractor.py          # DOCX parsing & field extraction
├── Exporter.py           # Excel export with styling
├── gen_demo.py           # Demo file generator
├── Templates/
│   └── index.html        # Web UI (responsive, dark mode)
└── demo_files/           # 30 sample DOCX files (mixed formats)
```

## 🔧 Customization

### Change Extraction Fields
Edit the `/extract` endpoint in `App.py`:
```python
fields = data.get("fields", [])  # User provides these via UI
```

### Modify Excel Styling
Update colors/fonts in `Exporter.py`:
```python
header_fill = PatternFill("solid", fgColor="1D9E75")  # Change color hex
```

### Adjust Document Format
Edit regex pattern in `Extractor.py`:
```python
pattern = rf"{escaped}\s*-\s*(.+?)(?:\r?\n|$)"  # Supports "Field - Value"
```

## 🧪 Testing
```bash
# Test extraction on demo files
python Extractor.py

# Expected output:
# 19/30 files fully extracted (with confidence = 1.0)
# 5/30 files intentionally showing 0.0 (to demo error handling)
# 6/30 files partial extraction
```

## 📝 Technical Details

### Extraction Algorithm
1. Load DOCX paragraphs
2. Join all text with newlines
3. For each requested field, search regex pattern `"FieldName - Value"`
4. Extract captured group (everything after dash)
5. Return dict with results + confidence = (found_fields / requested_fields)

### Confidence Scoring
- **1.0** = All requested fields found
- **0.5** = Half of requested fields found
- **0.0** = No fields found (graceful failure)
- **Helps identify extraction quality** without throwing errors

## 🎓 Lessons Demonstrated
- ✅ **Regex-based extraction** for semi-structured text
- ✅ **Excel automation** with professional formatting
- ✅ **Flask REST API** design
- ✅ **Error handling & graceful degradation**
- ✅ **Responsive web UI** with dark mode
- ✅ **Batch processing** at scale
- ✅ **Real-world robustness** (handles variant formats)

## 👥 Team
HackIndia Spark 4 — NCR East Region | Team: **Arise**

## 📄 License
MIT License

---

**Built for HackIndia Evaluation Round 2** | *Intelligent extraction, production-grade reliability*
