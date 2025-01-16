import hashlib
import unicodedata
from datetime import datetime

import cutlet

katsu = cutlet.Cutlet()

# TODO move to database?
hiragana_name_overrides = {"あいみょん": "Aimyon", "リーガルリリー": "Regal Lily"}


def convert_ts_to_local_dt(ts: str) -> str:
    return (
        datetime.fromtimestamp(int(ts))
        .astimezone(datetime.now().astimezone().tzinfo)
        .strftime("%H:%M:%S")
    )


def convert_japanese_to_romanji(text: str) -> str:
    if text in hiragana_name_overrides:
        return hiragana_name_overrides[text]

    if string_is_hiragana(text) or has_unicode_group(text):
        return katsu.romaji(text)

    return text


def string_is_hiragana(s: str) -> bool:
    def char_is_hiragana(c) -> bool:
        return "\u3040" <= c <= "\u309f"

    return all(char_is_hiragana(c) for c in s)


def generate_cuid2() -> str:
    from typing import Callable
    from cuid2 import cuid_wrapper

    cuid_generator: Callable[[], str] = cuid_wrapper()
    return cuid_generator()


def get_today_at_midnight() -> int:
    """
    Builds and returns the date for today at midnight as a timestamp
    :return: An integer timestamp
    """
    return int(
        datetime.now().replace(hour=0, minute=0, second=0, microsecond=0).timestamp()
    )


def has_unicode_group(text):
    for char in text:
        for name in (
            "CJK",
            "CHINESE",
            "KATAKANA",
            "HANGUL",
        ):
            if name in unicodedata.name(char):
                return True
    return False


def build_sort_name(name: str) -> str:
    converted = convert_japanese_to_romanji(name)
    return remove_articles(converted.lower())


def hash_string(text: str) -> str:
    return hashlib.sha3_256(text.encode()).hexdigest()


def remove_articles(text: str) -> str:
    split = text.split(" ")
    if len(split) == 1:
        return text

    if split[0] in ["The", "A", "An", "the", "a", "an"]:
        return text.replace(split[0], "").strip()
    else:
        return text


def remove_duplicates(items, key=None):
    unique_items = set()
    for item in items:
        val = item if key is None else key(item)
        if val not in unique_items:
            yield item
            unique_items.add(val)
