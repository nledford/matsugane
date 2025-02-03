import hashlib
import unicodedata
from datetime import datetime

import cutlet

katsu = cutlet.Cutlet()

# TODO move to database?
hiragana_name_overrides = {"あいみょん": "Aimyon", "リーガルリリー": "Regal Lily"}


def convert_ts_to_dt(ts: str | int) -> datetime:
    return datetime.fromtimestamp((int(ts))).astimezone(
        datetime.now().astimezone().tzinfo
    )


def convert_ts_to_local_time(ts: str | int) -> str:
    """
    Converts a unix timestamp to local time.

    :param ts: The unix timestamp to convert.
    :return: The unix timestamp converted to local time.

    >>> convert_ts_to_local_time("449802511")
    '20:08:31'
    >>> convert_ts_to_local_time(449802511)
    '20:08:31'
    >>> '00:00:00' == convert_ts_to_local_time("474747474")
    False

    """
    return convert_ts_to_dt(ts).strftime("%H:%M:%S")


def convert_japanese_to_romanji(text: str) -> str:
    if text in hiragana_name_overrides:
        return hiragana_name_overrides[text]

    if string_is_hiragana(text) or has_unicode_group(text):
        return katsu.romaji(text)

    return text


def string_is_hiragana(s: str) -> bool:
    """
    Check if a string is composed entirely of hiragana
    :param s: A string to check
    :return: True if the string is composed entirely of hiragana

    >>> string_is_hiragana("おはようございます")
    True
    >>> string_is_hiragana("Good morning!")
    False
    """

    def char_is_hiragana(c) -> bool:
        """
        Checks if a single character represents a hiragana
        :param c: A single character to check
        :return: True if the character represents a hiragana

        >>> char_is_hiragana("あ")
        True
        >>> char_is_hiragana("A")
        False
        """
        return "\u3040" <= c <= "\u309f"

    return all(char_is_hiragana(c) for c in s)


def get_today_at_midnight() -> int:
    """
    Builds and returns the date for today at midnight as a timestamp
    :return: An integer timestamp
    """
    return int(
        datetime.now().replace(hour=0, minute=0, second=0, microsecond=0).timestamp()
    )


def has_unicode_group(text: str) -> bool:
    """
    Detects if a provided string contains Japanese characters (Kanji, katana, or hiragana)

    >>> has_unicode_group("Rush")
    False
    >>> has_unicode_group("羊文学")
    True

    :param text: The string to check
    :return: True if string contains Japanese characters, False otherwise
    """
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
    converted = convert_japanese_to_romanji(name.lower())
    return remove_articles(converted.lower())


def hash_string(text: str) -> str:
    return hashlib.sha3_256(text.strip().encode()).hexdigest()


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


def get_last_refresh() -> str:
    """
    Constructs a string for the last refresh time.
    :return: The last refresh time.

    >>> expected = f"Last Refresh: {datetime.now().strftime('%H:%M:%S')}"
    >>> get_last_refresh() == expected
    True
    """
    return f"Last Refresh: {datetime.now().strftime('%H:%M:%S')}"
