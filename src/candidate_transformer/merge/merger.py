"""
Merge engine.

Combines structured CSV data and unstructured recruiter notes
into canonical candidate records with provenance and confidence.
"""

import hashlib

from candidate_transformer.models.candidate import (
    Candidate,
    Experience,
    ProvenanceEntry,
    Skill,
)
from candidate_transformer.models.source import CsvCandidate, NotesCandidate
from candidate_transformer.normalizers.phone import normalize_phone
from candidate_transformer.normalizers.skills import normalize_skill


CSV_CONFIDENCE = 0.95
NOTES_CONFIDENCE = 0.75


def _generate_candidate_id(name: str | None, email: str | None) -> str:
    """Generate deterministic candidate ID from stable candidate data."""
    raw_key = f"{name or ''}|{email or ''}".lower().strip()
    return hashlib.sha256(raw_key.encode("utf-8")).hexdigest()[:12]


def _build_provenance(
    field: str,
    value: str,
    source: str,
    method: str = "direct",
) -> ProvenanceEntry:
    """Create a provenance entry."""
    return ProvenanceEntry(
        field=field,
        value=value,
        source=source,
        method=method,
    )


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

        provenance: list[ProvenanceEntry] = []

        if csv_candidate.name:
            provenance.append(
                _build_provenance("full_name", csv_candidate.name, "csv")
            )

        if csv_candidate.email:
            provenance.append(
                _build_provenance("emails", csv_candidate.email, "csv")
            )

        normalized_phone = normalize_phone(csv_candidate.phone)

        if normalized_phone:
            provenance.append(
                _build_provenance("phones", normalized_phone, "csv")
            )

        experience: list[Experience] = []

        if csv_candidate.current_company or csv_candidate.title:
            experience.append(
                Experience(
                    company=csv_candidate.current_company,
                    title=csv_candidate.title,
                    summary="Current role from recruiter CSV export.",
                )
            )

            if csv_candidate.current_company:
                provenance.append(
                    _build_provenance(
                        "experience.company",
                        csv_candidate.current_company,
                        "csv",
                    )
                )

            if csv_candidate.title:
                provenance.append(
                    _build_provenance(
                        "experience.title",
                        csv_candidate.title,
                        "csv",
                    )
                )

        skills: list[Skill] = []

        if note_candidate:
            for skill_name in note_candidate.skills:
                normalized_skill = normalize_skill(skill_name)

                skills.append(
                    Skill(
                        name=normalized_skill,
                        confidence=NOTES_CONFIDENCE,
                        sources=["recruiter_notes"],
                    )
                )

                provenance.append(
                    _build_provenance(
                        "skills",
                        normalized_skill,
                        "recruiter_notes",
                        method="keyword_match",
                    )
                )

            if note_candidate.notes:
                provenance.append(
                    _build_provenance(
                        "summary",
                        note_candidate.notes,
                        "recruiter_notes",
                        method="free_text",
                    )
                )

        candidate = Candidate(
            candidate_id=_generate_candidate_id(
                csv_candidate.name,
                csv_candidate.email,
            ),
            full_name=csv_candidate.name,
            emails=[csv_candidate.email] if csv_candidate.email else [],
            phones=[normalized_phone] if normalized_phone else [],
            headline=csv_candidate.title,
            skills=skills,
            experience=experience,
            provenance=provenance,
            overall_confidence=0.85 if note_candidate else 0.75,
        )

        merged.append(candidate)

    return merged