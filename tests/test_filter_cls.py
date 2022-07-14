#
#  Copyright © 2022 CloudBlue LLC. All rights reserved.
#

from django_mongoengine import Document, EmbeddedDocument, fields
from py_rql.constants import FilterLookups

from dj_mongoengine_rql.filter_cls import MongoengineRQLFilterClass


class EmbDoc(EmbeddedDocument):
    str_f = fields.StringField()
    int_f = fields.IntField(blank=True)


class Doc(Document):
    str_f = fields.StringField(max_length=255, blank=True)
    bl = fields.BooleanField(default=True)
    dt = fields.DateTimeField(blank=True)
    d = fields.DateField(blank=True)
    dec = fields.DecimalField(blank=True)
    flt = fields.FloatField(blank=True)
    int_f = fields.IntField(blank=True)

    related_doc = fields.EmbeddedDocumentField('EmbDoc', blank=True)


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
