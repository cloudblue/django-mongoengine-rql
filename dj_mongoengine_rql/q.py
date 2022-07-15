#
#  Copyright © 2022 CloudBlue LLC. All rights reserved.
#

from mongoengine import Q as ME_Q
from mongoengine.queryset.transform import query


class Q(ME_Q):
    MODEL = None

    def __invert__(self):
        result = self.__class__(__raw__={'$nor': [query(_doc_cls=self.MODEL, **self.query)]})

        return result
