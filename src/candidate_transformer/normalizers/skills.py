CANONICAL_SKILLS = {
    "python": "Python",
    "fastapi": "FastAPI",
    "aws": "AWS",
    "genai": "Generative AI",
    "nlp": "Natural Language Processing",
}


def normalize_skill(skill: str) -> str:
    """Return canonical skill name."""

    return CANONICAL_SKILLS.get(
        skill.strip().lower(),
        skill.strip(),
    )