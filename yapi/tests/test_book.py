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
    # print(b)


def test_empty_book():
    b = book()
    assert b.__dict__ == {}


def test_iter_repetition():
    b = book(test_kwargs)
    expected_result = ['a', 'f']
    result = []
    for k in b:
        print(k)
        result.append(k)
    
    assert result == expected_result

    # two times the same result
    result = []
    for k in b:
        print(k)
        result.append(k)
    
    assert result == expected_result


def test_iter_repetition():
    b = book(test_kwargs)
    expected_result = ['a', 'b', 'c', 'd', 'e',
                       'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n']
    result = []
    for k in b:
        print('key', k)
        result.append(k)
    
    assert result == expected_result
