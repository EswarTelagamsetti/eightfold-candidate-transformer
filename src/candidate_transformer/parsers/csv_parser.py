"""
CSV parser.

Reads candidate data from CSV files and converts each row
into a CsvCandidate model.
"""

import csv
from pathlib import Path

from candidate_transformer.models.source import CsvCandidate


def parse_csv(csv_path: Path) -> list[CsvCandidate]:
    """Parse a CSV file into a list of CsvCandidate objects."""

    candidates: list[CsvCandidate] = []

    with csv_path.open("r", encoding="utf-8", newline="") as file:
        reader = csv.DictReader(file)

        for row in reader:
            candidates.append(
                CsvCandidate(
                    name=row.get("name"),
                    email=row.get("email"),
                    phone=row.get("phone"),
                    current_company=row.get("current_company"),
                    title=row.get("title"),
                )
            )

    return candidates