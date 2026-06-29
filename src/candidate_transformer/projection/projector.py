"""
Projection engine.

Converts internal canonical Candidate objects into configurable
output dictionaries based on runtime configuration.
"""

from typing import Any

from candidate_transformer.models.candidate import Candidate


def _get_value_by_path(candidate: Candidate, path: str) -> Any:
    """Read a value from Candidate using a simple config path."""

    if path == "full_name":
        return candidate.full_name

    if path == "emails":
        return candidate.emails

    if path == "emails[0]":
        return candidate.emails[0] if candidate.emails else None

    if path == "phones":
        return candidate.phones

    if path == "phones[0]":
        return candidate.phones[0] if candidate.phones else None

    if path == "skills":
        return [skill.model_dump() for skill in candidate.skills]

    if path == "skills[].name":
        return [skill.name for skill in candidate.skills]

    if path == "experience":
        return [experience.model_dump() for experience in candidate.experience]

    if path == "education":
        return [education.model_dump() for education in candidate.education]

    if path == "provenance":
        return [entry.model_dump() for entry in candidate.provenance]

    if path == "overall_confidence":
        return candidate.overall_confidence

    if path == "candidate_id":
        return candidate.candidate_id

    if path == "headline":
        return candidate.headline

    return None


def project_candidate(candidate: Candidate, config: dict[str, Any]) -> dict[str, Any]:
    """Project a Candidate into custom output shape using config."""

    output: dict[str, Any] = {}
    on_missing = config.get("on_missing", "null")

    for field_config in config.get("fields", []):
        output_path = field_config["path"]
        source_path = field_config.get("from", output_path)

        value = _get_value_by_path(candidate, source_path)

        if value is None:
            if field_config.get("required") and on_missing == "error":
                raise ValueError(f"Missing required field: {output_path}")

            if on_missing == "omit":
                continue

            output[output_path] = None
        else:
            output[output_path] = value

    if config.get("include_confidence", False):
        output["overall_confidence"] = candidate.overall_confidence

    if config.get("include_provenance", True):
        output["provenance"] = [
            entry.model_dump() for entry in candidate.provenance
        ]

    return output


def project_candidates(
    candidates: list[Candidate],
    config: dict[str, Any],
) -> list[dict[str, Any]]:
    """Project multiple candidates."""

    return [project_candidate(candidate, config) for candidate in candidates]