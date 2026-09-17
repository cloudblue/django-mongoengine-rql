#
#  Copyright © 2022 CloudBlue LLC. All rights reserved.
#

from mongoengine import Document, EmbeddedDocument, fields


class EmbDoc(EmbeddedDocument):
    str_f = fields.StringField(required=True)
    int_f = fields.IntField(required=False)


class Doc(Document):
    str_f = fields.StringField(max_length=255, required=False)
    bl = fields.BooleanField(default=True)
    dt = fields.DateTimeField(required=False)
    d = fields.DateField(required=False)
    dec = fields.DecimalField(required=False)
    flt = fields.FloatField(required=False)
    int_f = fields.IntField(required=False, db_field='other_int_f')

    related_doc = fields.EmbeddedDocumentField('EmbDoc', required=False)
