"""
Candidate data model.

Defines the canonical representation of a candidate after
information from multiple sources has been merged.
"""

from typing import Optional

from pydantic import BaseModel, Field


class Candidate(BaseModel):
    """Canonical representation of a candidate."""

    full_name: Optional[str] = None
    emails: list[str] = Field(default_factory=list)
    phones: list[str] = Field(default_factory=list)
    skills: list[str] = Field(default_factory=list)

    experience: Optional[str] = None
    education: Optional[str] = None
    summary: Optional[str] = None
    notes: Optional[str] = None