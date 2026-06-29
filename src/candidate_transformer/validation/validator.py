"""
Validation module.

Performs basic validation on canonical Candidate objects.
"""

from candidate_transformer.models.candidate import Candidate


def validate_candidate(candidate: Candidate) -> list[str]:
    """Validate a candidate and return validation errors."""

    errors: list[str] = []

    if not candidate.full_name:
        errors.append("Missing full name.")

    if not candidate.emails:
        errors.append("Missing email.")

    if not candidate.phones:
        errors.append("Missing phone number.")

    return errors


def validate_candidates(
    candidates: list[Candidate],
) -> dict[str, list[str]]:
    """Validate multiple candidates."""

    results: dict[str, list[str]] = {}

    for candidate in candidates:
        candidate_id = candidate.candidate_id or "unknown"
        results[candidate_id] = validate_candidate(candidate)

    return results