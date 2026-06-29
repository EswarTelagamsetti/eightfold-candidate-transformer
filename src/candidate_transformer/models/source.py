"""
Source-specific data models.

These models represent data extracted from individual sources
before it is merged into the canonical candidate model.
"""

from pydantic import BaseModel, Field


class CsvCandidate(BaseModel):
    """Candidate data extracted from a structured CSV source."""

    name: str | None = None
    email: str | None = None
    phone: str | None = None
    current_company: str | None = None
    title: str | None = None


class NotesCandidate(BaseModel):
    """Candidate data extracted from unstructured recruiter notes."""

    name: str | None = None
    email: str | None = None
    phone: str | None = None
    skills: list[str] = Field(default_factory=list)
    notes: str | None = None