# Eightfold Candidate Transformer

A production-style candidate transformation pipeline that converts heterogeneous candidate information into a configurable canonical representation.

This project was built as part of the Eightfold Engineering Assignment.

---

## Features

- Parse candidate information from CSV files
- Parse recruiter notes from free-text documents
- Merge structured and unstructured data
- Normalize phone numbers
- Normalize skill names
- Track provenance for every field
- Compute confidence scores
- Configurable JSON output projection
- Validation engine
- Command-line interface
- Unit tested using pytest

---

## Project Structure

```
src/
    candidate_transformer/
        config/
        merge/
        models/
        normalizers/
        parsers/
        projection/
        validation/
        main.py

sample_data/

outputs/

tests/

README.md
```

---

## Architecture

```text
CSV File            Recruiter Notes
   |                       |
   v                       v
CSV Parser            Notes Parser
   |                       |
   v                       v
CsvCandidate       NotesCandidate
        \             /
         \           /
          v         v
          Merge Engine
               |
               v
       Canonical Candidate
               |
               v
          Validation
               |
               v
          Projection
               |
               v
          JSON Output


## Installation

Clone repository

```bash
git clone https://github.com/EswarTelagamsetti/eightfold-candidate-transformer.git

cd eightfold-candidate-transformer
```

Create virtual environment

```bash
python -m venv .venv
```

Activate

Windows

```bash
.venv\Scripts\activate
```

Install dependencies

```bash
pip install -r requirements.txt
```

---

## Usage

Default projection

```bash
python -m candidate_transformer.main ^
--csv sample_data/candidates.csv ^
--notes sample_data/recruiter_notes.txt ^
--config sample_data/default_config.json ^
--output outputs/default_output.json
```

Custom projection

```bash
python -m candidate_transformer.main ^
--csv sample_data/candidates.csv ^
--notes sample_data/recruiter_notes.txt ^
--config sample_data/custom_config.json ^
--output outputs/custom_output.json
```

---

## Configuration

Projection is completely configuration-driven.

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

No code changes are required when the output schema changes.

---

## Validation

Current validation checks include

- Missing email
- Missing phone number

---

## Normalization

Phone

```
98765 43210
```

↓

```
+919876543210
```

Skills

```
python
```

↓

```
Python
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

## Provenance

Each output field stores

- source
- field
- extraction method

Example

```json
{
    "field":"skills",
    "value":"Python",
    "source":"recruiter_notes",
    "method":"keyword_match"
}
```

---

## Testing

Run all tests

```bash
pytest -v
```

Current status

```
9 tests passed
```

---

## Technologies

- Python 3.13
- Pydantic v2
- Pytest

---

## Future Improvements

- Fuzzy candidate matching
- Email-based merge strategy
- LLM-assisted information extraction
- Better confidence scoring
- REST API
- Docker support
- CI/CD pipeline

---

## Author

Eswar Telagamsetti