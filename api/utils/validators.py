from typing import Iterable


def validate_required_keys(payload: dict, required_keys: Iterable[str]) -> list[str]:
    return [key for key in required_keys if key not in payload]
