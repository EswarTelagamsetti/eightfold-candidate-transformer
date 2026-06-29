"""
Recruiter notes parser.

Parses semi-structured recruiter notes into NotesCandidate objects.
"""

from pathlib import Path
import re

from candidate_transformer.models.source import NotesCandidate


KNOWN_SKILLS = [
    "python",
    "fastapi",
    "aws",
    "genai",
    "nlp",
]


def _extract_skills(text: str) -> list[str]:
    """Extract known skills from recruiter notes."""

    text = text.lower()

    skills = []

    for skill in KNOWN_SKILLS:
        if skill in text:
            skills.append(skill)

    return skills


def parse_notes(notes_path: Path) -> list[NotesCandidate]:
    """Parse recruiter notes."""

    text = notes_path.read_text(encoding="utf-8")

    sections = [
        section.strip()
        for section in re.split(r"-{5,}", text)
        if section.strip()
    ]

    candidates: list[NotesCandidate] = []

    for section in sections:

        name = None
        email = None
        phone = None

        note_lines = []

        for line in section.splitlines():

            line = line.strip()

            if not line:
                continue

            if line.startswith("Candidate:"):
                name = line.replace("Candidate:", "").strip()

            elif line.startswith("Email:"):
                email = line.replace("Email:", "").strip()

            elif line.startswith("Phone:"):
                phone = line.replace("Phone:", "").strip()

            else:
                note_lines.append(line)

        notes = " ".join(note_lines)

        candidates.append(
            NotesCandidate(
                name=name,
                email=email,
                phone=phone,
                skills=_extract_skills(notes),
                notes=notes if notes else None,
            )
        )

    return candidates