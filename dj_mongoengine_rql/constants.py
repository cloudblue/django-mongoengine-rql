#
#  Copyright © 2022 Ingram Micro. All rights reserved.
#

from dj_rql.constants import FilterTypes
from mongoengine import fields


class MongoengineFilterTypes(FilterTypes):
    mapper = [
        (fields.BooleanField, FilterTypes.BOOLEAN),
        (fields.DateField, FilterTypes.DATE),
        (fields.DateTimeField, FilterTypes.DATETIME),
        (fields.DecimalField, FilterTypes.DECIMAL),
        (fields.FloatField, FilterTypes.FLOAT),
        (fields.IntField, FilterTypes.INT),
        (fields.StringField, FilterTypes.STRING),
    ]
