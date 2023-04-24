#
#  Copyright © 2023 Ingram Micro. All rights reserved.
#

from dj_rql.constants import DjangoLookups
from dj_rql.filter_cls import RQLFilterClass
from django_mongoengine.fields.djangoflavor import DjangoField
from py_rql.constants import FilterLookups

from dj_mongoengine_rql.constants import MongoengineFilterTypes
from dj_mongoengine_rql.q import Q


class MongoengineRQLFilterClass(RQLFilterClass):
    Q_CLS = Q
    FILTER_TYPES_CLS = MongoengineFilterTypes

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__class__.Q_CLS.MODEL = self.__class__.MODEL

    @classmethod
    def _is_valid_model_cls(cls, model):
        return True

    @classmethod
    def _is_field_supported(cls, field):
        return isinstance(field, DjangoField)

    @classmethod
    def _is_field_nullable(cls, field):
        return field.blank or field.primary_key

    @classmethod
    def _get_field_related_model(cls, field):
        return field.document_type

    @classmethod
    def _get_decimal_field_precision(cls, field):
        return field.precision

    def _build_django_q(self, filter_item, django_lookup, filter_lookup, typed_value):
        if django_lookup in (DjangoLookups.EXACT, DjangoLookups.NULL):
            v = typed_value if django_lookup == DjangoLookups.EXACT else None
            q = self.Q_CLS(**{filter_item['orm_route']: v})
            return ~q if filter_lookup == FilterLookups.NE else q

        if filter_lookup != FilterLookups.NE:
            kwargs = {'{0}__{1}'.format(filter_item['orm_route'], django_lookup): typed_value}
        else:
            kwargs = {'{0}__not__{1}'.format(filter_item['orm_route'], django_lookup): typed_value}

        return self.Q_CLS(**kwargs)
