# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import json
import random
import string
from typing import List
from ordered_set import OrderedSet

charset_upper = set(string.uppercase)
charset_lower = set(string.lowercase)
charset_alpha = set.union(charset_upper, charset_lower)
charset_digits = set(string.digits)
charset_symbols = set("!%@#&^*")
charset_banned = set("1lIO0")
charset = set.union(
    charset_upper,
    charset_lower,
    charset_digits,
    charset_symbols,
).difference(charset_banned)
charset_list = list(charset)


def is_valid_password(password): # pragma: no cover
    has_lower = len(set(password).intersection(charset_lower)) > 0
    has_upper = len(set(password).intersection(charset_upper)) > 0
    has_digits = len(set(password).intersection(charset_digits)) > 0
    has_symbol = len(set(password).intersection(charset_symbols)) > 0
    startswith_alpha = password[0] in charset_alpha
    return has_lower and has_upper and has_digits and has_symbol and startswith_alpha


def random_password(length): # pragma: no cover
    password = "".join([random.choice(charset_list) for _ in range(length)])
    if not is_valid_password(password):
        return random_password(length)
    return password


def tokenize(text, space_only=False):
    """

    :rtype text: List[str]
    """
    if space_only is False:
        text = text.replace("-", " ").replace("_", " ")
    tokens = [token for token in text.split(" ") if token.strip()]
    return tokens


def json_dumps(dct): # pragma: no cover
    return json.dumps(dct, encoding="utf-8", ensure_ascii=False)


def json_loads(dct): # pragma: no cover
    return json.loads(dct, encoding="utf-8")


def union(*lst_of_lst):
    s = OrderedSet(lst_of_lst[0])
    for l in lst_of_lst[1:]:
        s |= OrderedSet(l)
    return list(s)


def intersect(*lst_of_lst):
    s = OrderedSet(lst_of_lst[0])
    for l in lst_of_lst[1:]:
        s &= OrderedSet(l)
    return list(s)
