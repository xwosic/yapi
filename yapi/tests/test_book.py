import pytest
from ..utils import book


test_kwargs = {
    'a': {
        'b': 2,
        'c': {
            'd': [4, 5, 6],
            'e': (7, 8, 9)
        }
    },
    'f': {
        'g': [
            {
                'h': 10
            },
            {
                'i': {
                    'j': 11,
                    'k': 12
                }
            }
        ]
    }
}


def test_book_creation_from_kwargs():
    b = book(**test_kwargs)
    assert b.a.b == 2
    assert b.a.c.d == [4, 5, 6]
    assert b.a.c.e == (7, 8, 9)
    assert b.f.g[0].h == 10
    assert b.f.g[1].i.j == 11
    assert b.c is None

    assert b['a']['b'] == 2
    assert b['a']['c']['d'] == [4, 5, 6]
    assert b['a']['c']['e'] == (7, 8, 9)
    assert b['f']['g'][0]['h'] == 10
    assert b['f']['g'][1]['i']['j'] == 11
    assert b['c'] is None


def test_book_str():
    b = book(**test_kwargs)
    print(b)