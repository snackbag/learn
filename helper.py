import hashlib
import secrets
import time


def millis() -> int:
    """
    :return: Returns the current time in milliseconds
    """
    return round(time.time() * 1000)


def has_keys(keys: list, check: dict) -> bool:
    return all(key in check for key in keys)


def create_password(original: str) -> list[str]:
    salt = secrets.token_hex(16)
    salted_password = salt + original
    hashed_password = hashlib.sha256(salted_password.encode()).hexdigest()

    return [salt, hashed_password]


def verify_password(salt: str, hashed_password: str, input_password: str) -> bool:
    salted_input_password = salt + input_password
    hashed_input_password = hashlib.sha256(salted_input_password.encode()).hexdigest()

    return hashed_input_password == hashed_password
