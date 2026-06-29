from pathlib import Path

from candidate_transformer.merge.merger import merge_candidates
from candidate_transformer.parsers.csv_parser import parse_csv
from candidate_transformer.parsers.notes_parser import parse_notes


def test_merge():
    merged = merge_candidates(
        parse_csv(Path("sample_data/candidates.csv")),
        parse_notes(Path("sample_data/recruiter_notes.txt")),
    )

    assert len(merged) == 5

    first = merged[0]

    assert first.full_name == "Aarav Mehta"
    assert first.skills[0].name == "Python"
    assert first.overall_confidence == 0.85