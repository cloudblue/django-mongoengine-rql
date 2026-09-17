#
#  Copyright © 2023 Ingram Micro. All rights reserved.
#

from dj_rql.constants import DjangoLookups
from dj_rql.filter_cls import RQLFilterClass
from django.core.exceptions import FieldDoesNotExist
from mongoengine.base import BaseField
from py_rql.constants import FilterLookups, RQL_EMPTY

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
        return isinstance(field, BaseField)

    @staticmethod
    def _is_blank(field):
        if hasattr(field, 'required'):
            return not field.required
        return getattr(field, 'blank', False)

    @classmethod
    def _is_field_nullable(cls, field):
        return cls._is_blank(field) or field.primary_key

    @classmethod
    def _get_field_related_model(cls, field):
        return field.document_type

    @classmethod
    def _get_decimal_field_precision(cls, field):
        return field.precision

    @classmethod
    def _get_model_field(cls, model, field_name):
        try:
            return model._fields[field_name]
        except KeyError:
            raise FieldDoesNotExist(
                '{0} has no field named {1!r}'.format(model.__name__, field_name),
            )

    @classmethod
    def _convert_value(cls, django_field, str_value, use_repr=False):
        if cls.remove_quotes(str_value) == RQL_EMPTY:
            ft = cls.FILTER_TYPES_CLS
            filter_type = ft.field_filter_type(django_field)
            if filter_type in (ft.STRING, ft.INT):
                if filter_type == ft.INT or not cls._is_blank(django_field):
                    raise ValueError
                return ''
        return super()._convert_value(django_field, str_value, use_repr=use_repr)

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
