"""
Parser for recruiter notes.

Extracts candidate names, inferred skills, and raw recruiter notes
from semi-structured text files.
"""

from pathlib import Path

from candidate_transformer.models.source import NotesCandidate

KNOWN_SKILLS = {
    "python": "Python",
    "fastapi": "FastAPI",
    "aws": "AWS",
    "nlp": "NLP",
    "genai": "GenAI",
    "sql": "SQL",
    "machine learning": "Machine Learning",
    "backend": "Backend Development",
    "data engineering": "Data Engineering",
}


def _extract_skills(text: str) -> list[str]:
    """Extract known skills mentioned in free-text recruiter notes."""
    text_lower = text.lower()
    skills = []

    for keyword, canonical_name in KNOWN_SKILLS.items():
        if keyword in text_lower:
            skills.append(canonical_name)

    return skills


def parse_notes(notes_path: Path) -> list[NotesCandidate]:
    """Parse recruiter notes into NotesCandidate objects."""
    text = notes_path.read_text(encoding="utf-8")
    blocks = text.strip().split("------------------------------------")

    candidates: list[NotesCandidate] = []

    for block in blocks:
        block = block.strip()

        if not block:
            continue

        lines = [line.strip() for line in block.splitlines() if line.strip()]

        name = None
        note_lines = []

        for line in lines:
            if line.startswith("Candidate:"):
                name = line.replace("Candidate:", "").strip()
            else:
                note_lines.append(line)

        notes = " ".join(note_lines)
        skills = _extract_skills(notes)

        candidates.append(
            NotesCandidate(
                name=name,
                skills=skills,
                notes=notes if notes else None,
            )
        )

    return candidates