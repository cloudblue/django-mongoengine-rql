#
#  Copyright © 2022 CloudBlue LLC. All rights reserved.
#

import pytest

from tests.documents import Doc


@pytest.fixture
def is_real_mongo(settings):
    is_real = bool(settings.MONGODB_DATABASES['default']['username'])

    if is_real:
        Doc.objects.all().delete()

    yield is_real
