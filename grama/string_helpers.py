__all__ = [
    "str_count",
    "str_detect",
    "str_extract",
    "str_locate",
    "str_replace",
    "str_replace_all",
    "str_sub",
    "str_split",
    "str_which",
]

import re

from grama import make_symbolic, pipe, valid_dist, param_dist, dfdelegate
from pandas import Series
from numpy import NaN, isnan

# ------------------------------------------------------------------------------
# String helpers
# - a straight port of stringr
# ------------------------------------------------------------------------------

## Detect matches
# --------------------------------------------------
@make_symbolic
def str_detect(string, pattern):
    """
    Detect the presence of a pattern match in a string.
    """
    try:
        ## Escape by raise if string is single string
        if isinstance(string, str):
            raise TypeError
        return Series([not (re.search(pattern, s) is None) for s in string])

    ## Single string
    except TypeError:
        return not (re.search(pattern, string) is None)


@make_symbolic
def str_locate(string, pattern):
    """
    Find the indices of all pattern matches.
    """
    try:
        if isinstance(string, str):
            raise TypeError
        return Series([[m.start(0) for m in re.finditer(pattern, s)] for s in string])

    except TypeError:
        return [m.start(0) for m in re.finditer(pattern, string)]


def _safe_index(l, i=0):
    try:
        return l[i]
    except IndexError:
        return NaN


@make_symbolic
def str_which(string, pattern):
    """
    Find the index of the first pattern match.
    """
    indices = str_locate(string, pattern)

    try:
        if isinstance(string, str):
            raise TypeError
        return Series([_safe_index(inds) for inds in indices])

    except TypeError:
        return _safe_index(indices)


@make_symbolic
def str_count(string, pattern):
    """
    Count the number of matches in a string.
    """
    indices = str_locate(string, pattern)

    try:
        if isinstance(string, str):
            raise TypeError
        return Series([len(ind) for ind in indices])

    except TypeError:
        return len(indices)


## Subset strings
# --------------------------------------------------
@make_symbolic
def str_sub(string, start=0, end=None):
    """Extract substrings"""
    try:
        if isinstance(string, str):
            raise TypeError
        return Series([s[start:end] for s in string])

    except TypeError:
        return string[start:end]


def _extract_or_empty(string, pattern):
    match = re.search(pattern, string)

    try:
        return match.group(0)
    except AttributeError:
        return ""


@make_symbolic
def str_extract(string, pattern):
    """Extract the first regex pattern match"""

    try:
        if isinstance(string, str):
            raise TypeError
        return Series([_extract_or_empty(s, pattern) for s in string])

    except TypeError:

        return _extract_or_empty(string, pattern)


## Mutate string
# --------------------------------------------------
@make_symbolic
def str_replace(string, pattern, replacement):
    """Replace the first matched pattern in each string."""

    try:
        if isinstance(string, str):
            raise TypeError
        return Series(
            [
                re.sub(pattern, replacement, s, count=1)
                for s in string
            ]
        )

    except TypeError:

        return re.sub(pattern, replacement, string, count=1)

@make_symbolic
def str_replace_all(string, pattern, replacement):
    """Replace all occurences of pattern in each string."""

    try:
        if isinstance(string, str):
            raise TypeError
        return Series(
            [
                re.sub(pattern, replacement, s)
                for s in string
            ]
        )

    except TypeError:

        return re.sub(pattern, replacement, string)


## Split
# --------------------------------------------------
@make_symbolic
def str_split(string, pattern, maxsplit=0):
    """Split string into list on pattern

    Args:
        string (str or iterable[str]): String(s) to split
        pattern (str): Regex pattern on which to split

    Kwargs:
        maxsplit (int): Maximum number of splits, or 0 for unlimited

    Returns
        str or iterable[str]: List (of lists) of strings

    """

    try:
        if isinstance(string, str):
            raise TypeError
        return Series(
            [
                re.split(pattern, s, maxsplit=maxsplit)
                for s in string
            ]
        )

    except TypeError:

        return re.split(pattern, string, maxsplit=maxsplit)
