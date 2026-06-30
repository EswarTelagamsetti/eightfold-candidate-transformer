# Eightfold Candidate Transformer

A production-style candidate transformation pipeline that converts heterogeneous candidate information from multiple sources into a configurable canonical JSON representation.

This project was developed as part of the **Eightfold Engineering Assignment**.

---

# Project Overview

Recruitment data is often distributed across structured sources such as CSV files and unstructured recruiter notes. Managing this information manually can result in duplicate records, inconsistent formatting, and incomplete candidate profiles.

The Candidate Transformer automatically integrates candidate information from multiple sources, intelligently merges candidate records, normalizes important fields, validates the generated profiles, and produces configurable JSON output suitable for downstream recruitment systems.

---

# Features

- Parse candidate information from CSV files
- Parse recruiter notes from free-text documents
- Merge structured and unstructured candidate data
- Generate canonical candidate profiles
- Normalize phone numbers
- Normalize skill names
- Track provenance for every extracted field
- Compute candidate confidence scores
- Configuration-driven JSON projection
- Candidate validation
- Command Line Interface (CLI)
- Unit tested using Pytest

---

# Project Structure

```
eightfold-candidate-transformer/
│
├── src/
│   └── candidate_transformer/
│       ├── config/
│       ├── merge/
│       ├── models/
│       ├── normalizers/
│       ├── parsers/
│       ├── projection/
│       ├── validation/
│       └── main.py
│
├── sample_data/
├── outputs/
├── tests/
├── requirements.txt
├── pyproject.toml
└── README.md
```

---

# System Architecture

```text
                           INPUT SOURCES
                   ┌──────────────────────────┐
                   │                          │
             candidates.csv          recruiter_notes.txt
                   │                          │
                   ▼                          ▼
             CSV Parser                Notes Parser
                   │                          │
                   ▼                          ▼
            CsvCandidate             NotesCandidate
                   │                          │
                   └────────────┬─────────────┘
                                │
                                ▼
                     Candidate Matching
                                │
                                ▼
                         Merge Engine
                                │
                                ▼
                    Canonical Candidate
                                │
                                ▼
                     Data Normalization
                                │
                                ▼
                        Data Validation
                                │
                                ▼
                  Configuration Projection
                                │
                                ▼
                     Configurable JSON Output
```

---

# Installation

Clone the repository

```bash
git clone https://github.com/EswarTelagamsetti/eightfold-candidate-transformer.git

cd eightfold-candidate-transformer
```

Create virtual environment

```bash
python -m venv .venv
```

Activate

### Windows

```bash
.venv\Scripts\activate
```

Install dependencies

```bash
pip install -r requirements.txt
```

---

# Usage

Set Python path

### Windows PowerShell

```powershell
$env:PYTHONPATH="src"
```

---

## Generate Default Output

```powershell
python -m candidate_transformer.main `
--csv sample_data/candidates.csv `
--notes sample_data/recruiter_notes.txt `
--config sample_data/default_config.json `
--output outputs/default_output.json
```

---

## Generate Custom Output

```powershell
python -m candidate_transformer.main `
--csv sample_data/candidates.csv `
--notes sample_data/recruiter_notes.txt `
--config sample_data/custom_config.json `
--output outputs/custom_output.json
```

---

# Configuration

The projection engine is completely configuration-driven.

Example

```json
{
  "fields": [
    {
      "path": "candidate_name",
      "from": "full_name"
    },
    {
      "path": "email",
      "from": "emails[0]"
    }
  ]
}
```

Changing only the configuration file automatically changes the generated JSON output without modifying the application code.

---

# Validation

Current validation rules include:

- Email must be present
- Phone number must be present

Validation results are included in the generated output.

---

# Normalization

### Phone Number

```
98765 43210
```

↓

```
+919876543210
```

### Skills

```
python
```

↓

```
Python
```

```
fastapi
```

↓

```
FastAPI
```

```
nlp
```

↓

```
Natural Language Processing
```

```
genai
```

↓

```
Generative AI
```

---

# Provenance Tracking

Each important field stores:

- Source
- Original Value
- Extraction Method

Example

```json
{
    "field": "skills",
    "value": "Python",
    "source": "recruiter_notes",
    "method": "keyword_match"
}
```

This provides complete traceability for every generated candidate profile.

---

# Example Output

```json
{
  "full_name": "Aarav Mehta",
  "primary_email": "aarav.mehta@techverse.ai",
  "phone": "+919876543210",
  "skills": [
    "Python",
    "FastAPI",
    "AWS"
  ],
  "overall_confidence": 0.85
}
```

---

# Testing

Run all tests

```bash
pytest -v
```

Current Status

```
9 tests passed
```

---

# Technologies Used

- Python 3.13
- Pydantic v2
- Pytest
- JSON
- CSV
- argparse
- hashlib

---

# Future Improvements

- Fuzzy candidate matching
- Semantic candidate matching using embeddings
- Resume PDF parsing
- LLM-assisted recruiter note extraction
- Improved confidence scoring
- REST API deployment
- Docker containerization
- CI/CD using GitHub Actions

---

# Author

**Eswar Telagamsetti**

Developed as part of the **Eightfold Engineering Assignment**.