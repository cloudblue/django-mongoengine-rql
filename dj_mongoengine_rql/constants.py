#
#  Copyright © 2022 CloudBlue LLC. All rights reserved.
#

from dj_rql.constants import FilterTypes
from django_mongoengine import fields


class MongoengineFilterTypes(FilterTypes):
    mapper = [
        (fields.BooleanField, FilterTypes.BOOLEAN),
        (fields.DateTimeField, FilterTypes.DATETIME),
        (fields.DateField, FilterTypes.DATE),
        (fields.DecimalField, FilterTypes.DECIMAL),
        (fields.FloatField, FilterTypes.FLOAT),
        (fields.IntField, FilterTypes.INT),
        (fields.StringField, FilterTypes.STRING),
    ]
