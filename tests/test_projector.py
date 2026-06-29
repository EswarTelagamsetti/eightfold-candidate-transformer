from pathlib import Path

from candidate_transformer.config.settings import load_config
from candidate_transformer.merge.merger import merge_candidates
from candidate_transformer.parsers.csv_parser import parse_csv
from candidate_transformer.parsers.notes_parser import parse_notes
from candidate_transformer.projection.projector import project_candidates


def test_projection():
    config = load_config(Path("sample_data/default_config.json"))

    candidates = merge_candidates(
        parse_csv(Path("sample_data/candidates.csv")),
        parse_notes(Path("sample_data/recruiter_notes.txt")),
    )

    projected = project_candidates(candidates, config)

    assert projected[0]["full_name"] == "Aarav Mehta"
    assert projected[0]["phone"] == "+919876543210"