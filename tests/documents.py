#
#  Copyright © 2022 CloudBlue LLC. All rights reserved.
#

from django_mongoengine import Document, EmbeddedDocument, fields


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
    int_f = fields.IntField(blank=True, db_field='other_int_f')

    related_doc = fields.EmbeddedDocumentField('EmbDoc', blank=True)
