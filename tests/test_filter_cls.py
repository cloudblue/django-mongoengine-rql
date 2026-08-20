#
#  Copyright © 2023 Ingram Micro. All rights reserved.
#

from typing import Pattern

import pytest
from dj_rql.fields import SelectField
from py_rql.constants import FilterLookups
from py_rql.exceptions import RQLFilterValueError

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

    assert qs._query == {'$nor': [{'other_int_f': 120}], 'other_int_f': 1}


def test_eq_str():
    _, qs = DocFilterClass(Doc.objects).apply_filters('str_f=x')

    assert qs._query == {'str_f': 'x'}


def test_like_str():
    _, qs = DocFilterClass(Doc.objects).apply_filters('like(str_f,*x*s*)')

    assert isinstance(qs._query['str_f'], Pattern)


def test_ne_str():
    _, qs = DocFilterClass(Doc.objects).apply_filters('str_f=ne=x')

    assert qs._query == {'$nor': [{'str_f': 'x'}]}


def test_null():
    _, qs = DocFilterClass(Doc.objects).apply_filters('flt=null()')

    assert qs._query == {'flt': None}


def test_not_null():
    _, qs = DocFilterClass(Doc.objects).apply_filters('flt=ne=null()')

    assert qs._query == {'$nor': [{'flt': None}]}


def test_db_operation(is_real_mongo):
    if is_real_mongo:
        doc = Doc.objects.create(str_f='a')
        Doc.objects.create(str_f='b')

        _, qs = DocFilterClass(Doc.objects).apply_filters('str_f=a')

        assert list(qs.all()) == [doc]


def test_select_field_is_field_supported_does_not_raise():
    field = SelectField()

    assert MongoengineRQLFilterClass._is_field_supported(field) is False


def test_select_field_is_field_nullable_does_not_raise():
    field = SelectField()

    assert MongoengineRQLFilterClass._is_field_nullable(field) is False


def test_empty_str_f():
    _, qs = DocFilterClass(Doc.objects).apply_filters('str_f=empty()')

    assert qs._query == {'str_f': ''}


def test_ne_empty_str_f():
    _, qs = DocFilterClass(Doc.objects).apply_filters('str_f=ne=empty()')

    assert qs._query == {'$nor': [{'str_f': ''}]}


def test_empty_int_f():
    with pytest.raises(RQLFilterValueError):
        DocFilterClass(Doc.objects).apply_filters('int_f=empty()')


def test_ne_empty_int_f():
    with pytest.raises(RQLFilterValueError):
        DocFilterClass(Doc.objects).apply_filters('int_f=ne=empty()')


def test_empty_dtf():
    with pytest.raises(RQLFilterValueError):
        DocFilterClass(Doc.objects).apply_filters('dtf=empty()')


def test_empty_d():
    with pytest.raises(RQLFilterValueError):
        DocFilterClass(Doc.objects).apply_filters('d=empty()')


def test_empty_dec():
    with pytest.raises(RQLFilterValueError):
        DocFilterClass(Doc.objects).apply_filters('dec=empty()')


def test_empty_flt():
    with pytest.raises(RQLFilterValueError):
        DocFilterClass(Doc.objects).apply_filters('flt=empty()')


def test_empty_bl():
    with pytest.raises(RQLFilterValueError):
        DocFilterClass(Doc.objects).apply_filters('bl=empty()')
