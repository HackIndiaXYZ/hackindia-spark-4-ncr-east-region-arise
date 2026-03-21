# ID-RSS — Intelligent Document Retrieval & Structuring System

[![Live Site](https://img.shields.io/badge/🌐%20Live%20Site-ID--RSS-1D9E75?style=for-the-badge)](https://ayushh-sharmaa.github.io/ARISE/) [![PPT](https://img.shields.io/badge/📊%20View-Presentation-B7472A?style=for-the-badge)](https://onedrive.live.com/edit?cid=cc1a3d34e76d2b04&id=CC1A3D34E76D2B04!s88384481f2fe44758a64580fbd32cf99&resid=CC1A3D34E76D2B04!s88384481f2fe44758a64580fbd32cf99&ithint=file%2Cpptx&embed=1&em=2&amp=&wdAr=1.7777777777777777&migratedtospo=true&redeem=aHR0cHM6Ly8xZHJ2Lm1zL3AvYy9jYzFhM2QzNGU3NmQyYjA0L0lRU0JSRGlJX3ZKMVJJcGtXQS05TXMtWkFYN05sb2N3MWJRdlVHSk55Qlg0akw0P2VtPTImYW1wO3dkQXI9MS43Nzc3Nzc3Nzc3Nzc3Nzc3&wdo=2)

## 🎯 Problem Statement
Organizations handle hundreds of student/employee documents (DOCX files) containing structured data scattered across paragraphs. Manual data extraction is slow, error-prone, and doesn't scale. **ID-RSS** automates this.

---

## 💡 The Real Cost of Manual Processing

Educational and research institutes spend enormous time opening files one by one, copying data by hand, and pasting it into databases. This creates three core problems — a drain on human resources for routine data entry, frequent data integrity failures due to inconsistent document formats, and severely delayed time-to-insight that slows down operations.

**ID-RSS eliminates all three.**

---

## ⚙️ How It Works

The system follows a simple four-step pipeline:

**Upload → Extract → Structure → Export**

Users provide a folder of raw `.docx` documents and define which fields they need. ID-RSS automatically scans every file using regex-based extraction, structures the results, and exports a clean Excel report — all in minutes, not hours.

Two built-in safeguards ensure reliability at every step. A **confidence scoring system** flags documents where extraction was partial or incomplete, and **graceful error handling** ensures the system never crashes on malformed or unexpected file formats — it simply marks missing data as `—` and moves on.

---

## ✨ Key Features

- **Scale** — Batch processes 30+ documents simultaneously
- **Speed** — Real-time extraction with confidence metrics per document
- **Flexibility** — Supports `.docx` and `.txt` formats with user-defined fields
- **Output** — Styled Excel export with summaries, auto-width columns, and color-coded headers
- **Interface** — Clean web UI with dark mode, no technical knowledge required

---

## 📁 Project Structure
```
ID-RSS/
├── App.py           # Flask server & REST API
├── Extractor.py     # DOCX parsing & regex field extraction
├── Exporter.py      # Styled Excel export
├── Templates/
│   └── index.html   # Web UI (responsive, dark mode)
└── demo_files/      # 30+ sample DOCX files (mixed formats)
```

---

## 📈 Impact

95% reduction in manual data entry. Scales to enterprise-level document processing across student records, admission documents, research data, and compliance documentation.

---

## 👥 Team ARISE
Tushar Goswami (Lead) · Tanishk Bansal · Ayush Sharma
HackIndia 2026 | Open Innovation Challenge

## 📄 License
MIT License
