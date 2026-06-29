"""
Merge engine.

Combines structured CSV data and unstructured recruiter notes
into one canonical candidate record with provenance and confidence.
"""

from candidate_transformer.models.candidate import Candidate
from candidate_transformer.models.source import CsvCandidate, NotesCandidate


def merge_candidates(
    csv_candidates: list[CsvCandidate],
    notes_candidates: list[NotesCandidate],
) -> list[Candidate]:
    """Merge CSV and recruiter-note candidates by candidate name."""

    notes_by_name = {
        candidate.name.lower(): candidate
        for candidate in notes_candidates
        if candidate.name
    }

    merged: list[Candidate] = []

    for csv_candidate in csv_candidates:
        note_candidate = None

        if csv_candidate.name:
            note_candidate = notes_by_name.get(csv_candidate.name.lower())

        candidate = Candidate(
            full_name=csv_candidate.name,
            emails=[csv_candidate.email] if csv_candidate.email else [],
            phones=[csv_candidate.phone] if csv_candidate.phone else [],
            skills=note_candidate.skills if note_candidate else [],
            experience=csv_candidate.title,
            summary=note_candidate.notes if note_candidate else None,
            notes=note_candidate.notes if note_candidate else None,
        )

        merged.append(candidate)

    return merged