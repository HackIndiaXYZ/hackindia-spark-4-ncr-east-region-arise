# ID-RSS — Intelligent Document Retrieval & Structuring System

[![Live Site](https://img.shields.io/badge/🌐%20Live%20Site-ID--RSS-1D9E75?style=for-the-badge)](https://ayushh-sharmaa.github.io/ARISE/) [![PPT](https://img.shields.io/badge/📊%20View-Presentation-B7472A?style=for-the-badge)](https://onedrive.live.com/edit?cid=cc1a3d34e76d2b04&id=CC1A3D34E76D2B04!s88384481f2fe44758a64580fbd32cf99&resid=CC1A3D34E76D2B04!s88384481f2fe44758a64580fbd32cf99&ithint=file%2Cpptx&embed=1&em=2&amp=&wdAr=1.7777777777777777&migratedtospo=true&redeem=aHR0cHM6Ly8xZHJ2Lm1zL3AvYy9jYzFhM2QzNGU3NmQyYjA0L0lRU0JSRGlJX3ZKMVJJcGtXQS05TXMtWkFYN05sb2N3MWJRdlVHSk55Qlg0akw0P2VtPTImYW1wO3dkQXI9MS43Nzc3Nzc3Nzc3Nzc3Nzc3&wdo=2)

## 🎯 Problem Statement
Organizations handle hundreds of student/employee documents (DOCX files) containing structured data scattered across paragraphs. Manual data extraction is slow, error-prone, and doesn't scale. **ID-RSS** automates this.

---

## 🚀 Quick Start
```bash
pip install flask python-docx openpyxl
python App.py
# Open http://localhost:5000
```

---

## ✨ What We Built

ID-RSS is a web-based document intelligence system that extracts structured data from bulk DOCX files and exports it as a clean, styled Excel report — no manual copy-pasting required.

Upload a folder of documents, define the fields you need, and get a downloadable Excel sheet in seconds.

---

## ⚙️ How It Works

### Step 1 — Document Parsing
Each `.docx` file is loaded and its paragraphs are joined into a single text block. For every requested field, a regex pattern searches for the format `FieldName - Value` and extracts the result. If a field is missing or malformed, it returns `—` instead of crashing.

### Step 2 — Confidence Scoring
Every extracted record gets a confidence score based on how many requested fields were successfully found. A score of `1.0` means all fields extracted cleanly. This helps identify problematic documents at a glance without manually reviewing each file.

### Step 3 — Excel Export
All extracted records are written to a styled `.xlsx` file with two sheets — a data table with frozen headers, alternating row colors, and auto-width columns, and a summary sheet with processing metadata like date, field count, and total records.

### Step 4 — Web Interface
A simple Flask web UI lets non-technical users point to a folder, specify fields, hit Extract, and download the result. No command line needed.

---

## 📁 Project Structure
```
ID-RSS/
├── App.py              # Flask server & REST API
├── Extractor.py        # DOCX parsing & regex extraction
├── Exporter.py         # Styled Excel export
├── gen_demo.py         # Demo file generator
├── Templates/
│   └── index.html      # Responsive web UI (dark mode)
└── demo_files/         # 30 sample DOCX files (mixed formats)
```

---

## 📊 Performance

| Files | Extract + Export Time |
|---|---|
| 30 files | < 5 seconds |
| Scales linearly with document count |

---

## 🧪 Test Cases

The `demo_files/` folder includes 30 documents — 19 with clean formatting (confidence 1.0), 5 intentionally malformed to demonstrate graceful error handling, and 6 with partial data to show confidence scoring in action.

---

## 👥 Team
HackIndia Spark 4 — NCR East Region | Team: **Arise**

## 📄 License
MIT License
