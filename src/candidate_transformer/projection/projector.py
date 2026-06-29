"""
Projection engine.

Converts internal canonical Candidate objects into configurable
output dictionaries based on runtime configuration.
"""

from typing import Any

from candidate_transformer.models.candidate import Candidate


def _to_plain_value(value: Any) -> Any:
    """Convert Pydantic models into plain Python values."""
    if hasattr(value, "model_dump"):
        return value.model_dump()

    if isinstance(value, list):
        return [_to_plain_value(item) for item in value]

    return value


def _get_attribute_value(obj: Any, attr: str) -> Any:
    """Safely read an attribute from an object or dictionary."""
    if isinstance(obj, dict):
        return obj.get(attr)

    return getattr(obj, attr, None)


def _resolve_path(obj: Any, path: str) -> Any:
    """
    Resolve simple paths like:
    - full_name
    - emails[0]
    - skills[].name
    - experience[].company
    """
    current = obj

    parts = path.split(".")

    for part in parts:
        if current is None:
            return None

        if part.endswith("[]"):
            attr = part[:-2]
            current = _get_attribute_value(current, attr)

            if not isinstance(current, list):
                return None

            remaining_path = ".".join(parts[parts.index(part) + 1:])

            if not remaining_path:
                return _to_plain_value(current)

            return [
                _resolve_path(item, remaining_path)
                for item in current
            ]

        if "[" in part and part.endswith("]"):
            attr, index_part = part[:-1].split("[")
            index = int(index_part)

            current = _get_attribute_value(current, attr)

            if not isinstance(current, list):
                return None

            if index >= len(current):
                return None

            current = current[index]
        else:
            current = _get_attribute_value(current, part)

    return _to_plain_value(current)


def project_candidate(candidate: Candidate, config: dict[str, Any]) -> dict[str, Any]:
    """Project a Candidate into custom output shape using config."""
    output: dict[str, Any] = {}
    on_missing = config.get("on_missing", "null")

    for field_config in config.get("fields", []):
        output_path = field_config["path"]
        source_path = field_config.get("from", output_path)

        value = _resolve_path(candidate, source_path)

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