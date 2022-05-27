from xml.dom.pulldom import default_bufsize
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
                    'k': 12,
                    'l': [
                        13, 
                        {
                            'm': {
                                'n': 14
                            }
                        }
                    ]
                }
            }
        ]
    }
}

test_list_of_dicts = [
    {
        'a': 1
    },
    {
        'b': {
            'c': [
                {
                    'd': {
                        'e': 2
                    }
                }
            ]
        }
    }
]


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


def test_book_creation_from_list_of_dicts():
    b = book(*test_list_of_dicts)
    assert b.a == 1
    assert b.b.c[0].d.e == 2

    assert b['a'] == 1
    assert b['b']['c'][0]['d']['e'] == 2


def test_book_str():
    b = book(**test_kwargs)
    assert str(b) == 'a|b: 2\n' \
                     'a|c|d: [4, 5, 6]\n' \
                     'a|c|e: (7, 8, 9)\n' \
                     'f|g: [{}, {}]\n' \
                     'f|g|[0]|h: 10\n' \
                     'f|g|[1]|i|j: 11\n' \
                     'f|g|[1]|i|k: 12\n' \
                     'f|g|[1]|i|l: [13, {}]\n' \
                     'f|g|[1]|i|l|[1]|m|n: 14\n'


def test_empty_book():
    b = book()
    assert b.__dict__ == {}


def test_iter_repetition():
    b = book(test_kwargs)
    expected_result = [
        'a',
        'a|b',
        'a|c',
        'a|c|d',
        'a|c|e',
        'f',
        'f|g',
        'f|g|[0]|h',
        'f|g|[1]|i',
        'f|g|[1]|i|j',
        'f|g|[1]|i|k',
        'f|g|[1]|i|l',
        'f|g|[1]|i|l|[1]|m',
        'f|g|[1]|i|l|[1]|m|n'
    ]
    result = []
    for k in b:
        result.append(k)
    
    assert result == expected_result

    # two times the same result
    result = []
    for k in b:
        result.append(k)
    
    assert result == expected_result


def test_iter():
    b = book(test_kwargs)
    expected_result = [
        'a',
        'a|b',
        'a|c',
        'a|c|d',
        'a|c|e',
        'f',
        'f|g',
        'f|g|[0]|h',
        'f|g|[1]|i',
        'f|g|[1]|i|j',
        'f|g|[1]|i|k',
        'f|g|[1]|i|l',
        'f|g|[1]|i|l|[1]|m',
        'f|g|[1]|i|l|[1]|m|n'
    ]
    result = []
    for k in b:
        result.append(k)
    
    assert result == expected_result


def test_iter_values():
    b = book(test_kwargs)
    expected_result = [2, 4, 5, 6, 7, 8, 9,
                       10, 11, 12, 13, 14]
    result = []
    for i in b.values():
        result.append(i)
    
    assert result == expected_result


def test_get_value():
    b = book(test_kwargs)

    result = b.get_value('f|g|[1]|i|l|[1]|m|n')

    assert result == 14

    result = b.get_value('a|c|d|[1]')

    assert result == 5


def test_get_values_in_loop():
    b = book(test_kwargs)

    result = []

    for k in b:
        r = b.get_value(k)
        result.append(r)
    
    assert result == [
        {},
        2,
        {},
        [4, 5, 6],
        (7, 8, 9),
        {},
        [{}, {}],
        10,
        {},
        11,
        12,
        [13, {}],
        {},
        14
    ]
