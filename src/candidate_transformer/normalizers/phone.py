import re


def normalize_phone(phone: str | None) -> str | None:
    """Convert phone numbers into E.164-like format."""

    if not phone:
        return None

    digits = re.sub(r"\D", "", phone)

    if len(digits) == 10:
        digits = "91" + digits

    return "+" + digits