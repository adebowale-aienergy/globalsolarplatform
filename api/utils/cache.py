from functools import lru_cache


@lru_cache(maxsize=128)
def cached_key(key: str) -> str:
    return key
