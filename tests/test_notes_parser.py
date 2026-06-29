from pathlib import Path

from candidate_transformer.parsers.notes_parser import parse_notes


def test_parse_notes():
    candidates = parse_notes(Path("sample_data/recruiter_notes.txt"))

    assert len(candidates) == 2

    assert candidates[0].name == "Aarav Mehta"
    assert candidates[0].email == "aarav.mehta@techverse.ai"
    assert candidates[0].phone == "+919876543210"

    assert "python" in candidates[0].skills
    assert "aws" in candidates[0].skills