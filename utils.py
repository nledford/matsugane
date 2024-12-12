import hashlib
from datetime import datetime


def get_today_at_midnight() -> int:
    """
    Builds and returns the date for today at midnight as a timestamp
    :return: An integer timestamp
    """
    return int(
        datetime
        .now()
        .replace(hour=0, minute=0, second=0, microsecond=0)
        .timestamp()
    )


def remove_articles(text: str) -> str:
    split = text.split(' ')
    if len(split) == 1:
        return text

    if split[0] in ['The', 'A', 'An', 'the', 'a', 'an']:
        return text.replace(split[0], '').strip()
    else:
        return text


def hash_str(text: str) -> str:
    return hashlib.sha3_256(text.encode('utf-8')).hexdigest()
