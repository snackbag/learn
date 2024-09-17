import time


def millis() -> int:
    """
    :return: Returns the current time in milliseconds
    """
    return round(time.time() * 1000)
