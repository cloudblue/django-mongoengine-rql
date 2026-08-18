#
#  Copyright © 2022 CloudBlue LLC. All rights reserved.
#

import mongomock
import pytest
from mongoengine.connection import register_connection

from tests.documents import Doc
from tests.settings import MONGODB_DATABASES


def _bootstrap_connection():
    for alias, conn_settings in MONGODB_DATABASES.items():
        conn_settings = dict(conn_settings)
        if not conn_settings.get('host'):
            conn_settings['host'] = 'mongodb://localhost'
            conn_settings['mongo_client_class'] = mongomock.MongoClient
        register_connection(alias, **conn_settings)


_bootstrap_connection()


@pytest.fixture
def is_real_mongo(settings):
    is_real = bool(settings.MONGODB_DATABASES['default']['username'])

    if is_real:
        Doc.objects.all().delete()

    yield is_real
