import time


def millis() -> int:
    """
    :return: Returns the current time in milliseconds
    """
    return round(time.time() * 1000)


def has_keys(keys: list, check: dict) -> bool:
    return all(key in check for key in keys)
