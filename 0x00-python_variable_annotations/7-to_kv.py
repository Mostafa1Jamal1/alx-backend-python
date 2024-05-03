#!/usr/bin/env python3


from typing import Union, Tuple


def to_kv(k: str, v: Union[int, float]) -> Tuple[str, float]:
    ''' returns a tuple
    The first element of the tuple is the string
    The second element is the square of the given number'''
    return tuple([k, v * v])
