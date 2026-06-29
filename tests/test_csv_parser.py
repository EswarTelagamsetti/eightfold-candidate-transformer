from pathlib import Path

from candidate_transformer.parsers.csv_parser import parse_csv


def test_parse_csv():
    candidates = parse_csv(Path("sample_data/candidates.csv"))

    assert len(candidates) == 5

    assert candidates[0].name == "Aarav Mehta"
    assert candidates[0].email == "aarav.mehta@techverse.ai"
    assert candidates[0].phone == "+919876543210"