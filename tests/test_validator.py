from pathlib import Path

from candidate_transformer.merge.merger import merge_candidates
from candidate_transformer.parsers.csv_parser import parse_csv
from candidate_transformer.parsers.notes_parser import parse_notes
from candidate_transformer.validation.validator import validate_candidates


def test_validator():
    candidates = merge_candidates(
        parse_csv(Path("sample_data/candidates.csv")),
        parse_notes(Path("sample_data/recruiter_notes.txt")),
    )

    result = validate_candidates(candidates)

    assert len(result) == 5

    for errors in result.values():
        assert errors == []