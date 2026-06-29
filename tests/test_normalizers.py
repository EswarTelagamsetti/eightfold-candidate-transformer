from candidate_transformer.normalizers.phone import normalize_phone
from candidate_transformer.normalizers.skills import normalize_skill


def test_phone_normalization():
    assert normalize_phone("98765 43210") == "+919876543210"


def test_skill_python():
    assert normalize_skill("python") == "Python"


def test_skill_fastapi():
    assert normalize_skill("FASTAPI") == "FastAPI"


def test_unknown_skill():
    assert normalize_skill("Docker") == "Docker"