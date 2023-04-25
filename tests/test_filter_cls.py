#
#  Copyright © 2023 Ingram Micro. All rights reserved.
#

from typing import Pattern

from py_rql.constants import FilterLookups

from dj_mongoengine_rql.filter_cls import MongoengineRQLFilterClass
from tests.documents import Doc


class DocFilterClass(MongoengineRQLFilterClass):
    MODEL = Doc
    SELECT = True
    FILTERS = (
        {
            'filter': 'str_f',
            'search': True,
        },
        'bl',
        {
            'filter': 'dtf',
            'source': 'dt',
            'ordering': True,
        },
        {
            'filter': 'd',
            'lookups': {FilterLookups.EQ},
        },
        {
            'filter': 'dec',
            'hidden': True,
        },
        'flt',
        'int_f',
        {
            'namespace': 'related',
            'source': 'related_doc',
            'filters': ('str_f',),
        },
        {
            'filter': 'r_int_f',
            'source': 'related_doc__int_f',
        },
    )


def test_init():
    _, qs = DocFilterClass(Doc.objects).apply_filters(
        'ordering(-dtf)&search=x&select(dec)&'
        '((str_f=ne=abc&bl=true)|(d=eq=2022-01-01&ge(dtf,2019-02-12T10:02Z)))&'
        'dec=lt=24.23&flt=2.1&not(eq(int_f,120))&'
        'related.str_f=abc&r_int_f=0',
    )

    assert list(qs.all()) == []


def test_not():
    _, qs = DocFilterClass(Doc.objects.filter(int_f=1)).apply_filters('not(eq(int_f,120))')

    assert qs.query.q == {'$nor': [{'other_int_f': 120}], 'other_int_f': 1}


def test_eq_str():
    _, qs = DocFilterClass(Doc.objects).apply_filters('str_f=x')

    assert qs.query.q == {'str_f': 'x'}


def test_like_str():
    _, qs = DocFilterClass(Doc.objects).apply_filters('like(str_f,*x*s*)')

    assert isinstance(qs.query.q['str_f'], Pattern)


def test_ne_str():
    _, qs = DocFilterClass(Doc.objects).apply_filters('str_f=ne=x')

    assert qs.query.q == {'$nor': [{'str_f': 'x'}]}


def test_null():
    _, qs = DocFilterClass(Doc.objects).apply_filters('flt=null()')

    assert qs.query.q == {'flt': None}


def test_not_null():
    _, qs = DocFilterClass(Doc.objects).apply_filters('flt=ne=null()')

    assert qs.query.q == {'$nor': [{'flt': None}]}


def test_db_operation(is_real_mongo):
    if is_real_mongo:
        doc = Doc.objects.create(str_f='a')
        Doc.objects.create(str_f='b')

        _, qs = DocFilterClass(Doc.objects).apply_filters('str_f=a')

        assert list(qs.all()) == [doc]
