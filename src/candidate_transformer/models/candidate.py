"""
Candidate data model.

Defines the canonical representation of a candidate after
information from multiple sources has been merged.
"""

from pydantic import BaseModel, Field


class ProvenanceEntry(BaseModel):
    field: str
    value: str
    source: str
    method: str = "direct"


class Skill(BaseModel):
    """Canonical skill representation with confidence and sources."""

    name: str
    confidence: float
    sources: list[str] = Field(default_factory=list)


class Experience(BaseModel):
    """Candidate experience entry."""

    company: str | None = None
    title: str | None = None
    start: str | None = None
    end: str | None = None
    summary: str | None = None


class Location(BaseModel):
    """Candidate location."""

    city: str | None = None
    region: str | None = None
    country: str | None = None


class Links(BaseModel):
    """Candidate profile links."""

    linkedin: str | None = None
    github: str | None = None
    portfolio: str | None = None
    other: list[str] = Field(default_factory=list)


class Education(BaseModel):
    """Candidate education entry."""

    institution: str | None = None
    degree: str | None = None
    field: str | None = None
    end_year: int | None = None


class Candidate(BaseModel):
    """Canonical representation of a candidate."""

    candidate_id: str | None = None
    full_name: str | None = None
    emails: list[str] = Field(default_factory=list)
    phones: list[str] = Field(default_factory=list)
    location: Location | None = None
    links: Links | None = None
    headline: str | None = None
    years_experience: float | None = None
    skills: list[Skill] = Field(default_factory=list)
    experience: list[Experience] = Field(default_factory=list)
    education: list[Education] = Field(default_factory=list)
    provenance: list[ProvenanceEntry] = Field(default_factory=list)
    overall_confidence: float = 0.0