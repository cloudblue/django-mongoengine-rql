# Django Mongoengine RQL

[![pyversions](https://img.shields.io/pypi/pyversions/django-mongoengine-rql.svg)](https://pypi.org/project/django-mongoengine-rql/)
[![PyPi Status](https://img.shields.io/pypi/v/django-mongoengine-rql.svg)](https://pypi.org/project/django-mongoengine-rql/)
[![PyPI status](https://img.shields.io/pypi/status/django-mongoengine-rql.svg)](https://pypi.org/project/django-mongoengine-rql/)
[![PyPI Downloads](https://img.shields.io/pypi/dm/django-mongoengine-rql)](https://pypi.org/project/django-mongoengine-rql/)
[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=django-mongoengine-rql&metric=alert_status)](https://sonarcloud.io/summary/new_code?id=django-mongoengine-rql)
[![Coverage](https://sonarcloud.io/api/project_badges/measure?project=django-mongoengine-rql&metric=coverage)](https://sonarcloud.io/summary/new_code?id=django-mongoengine-rql)


## Introduction

RQL (Resource query language) is designed for modern application development. It is built for the web, ready for NoSQL, and highly extensible with simple syntax.
This is a query language for fast and convenient database interaction. RQL was designed for use in URLs to request object-style data structures.

This library is a Django-Mongoengine specific implementation of RQL filtering.

[RQL Reference](https://connect.cloudblue.com/community/api/rql/)

[Django RQL](https://github.com/cloudblue/django-rql)

[Django Mongoengine](https://github.com/MongoEngine/django-mongoengine)

## Install

`Django Mongoengine RQL` can be installed from [pypi.org](https://pypi.org/project/django-mongoengine-rql/) using pip:

```
$ pip install django-mongoengine-rql
```

## Documentation

This library is fully based on [Django RQL](https://github.com/cloudblue/django-rql), so there are no specific docs for it.
Full documentation for Django-RQL is available at [https://django-rql.readthedocs.org](https://django-rql.readthedocs.org).

## Example

```python
# filters.py
from dj_mongoengine_rql.filter_cls import MongoengineRQLFilterClass
from py_rql.constants import FilterLookups
from your_docs import Document

class DocFilters(MongoengineRQLFilterClass):
    MODEL = Document
    SELECT = True
    FILTERS = (
        'filter1',
        {
            'filter': 'filter2',
            'source': 'related_doc__doc_field',
        },
        {
            'namespace': 'ns1',
            'filters': ('ns1f',),
        },
        {
            'filter': 'filter3',
            'lookups': {FilterLookups.EQ, FilterLookups.IN},
        },
    )


# views.py
from dj_rql.drf.backend import RQLFilterBackend
from dj_rql.drf.paginations import RQLContentRangeLimitOffsetPagination
from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet

class DRFViewSet(mixins.ListModelMixin, GenericViewSet):
    queryset = Document.objects.all()
    rql_filter_class = DocFilters
    pagination_class = RQLContentRangeLimitOffsetPagination
    filter_backends = (RQLFilterBackend,)

```

## Notes

Due to implementation and Mongo engine features there may be some limitations in filtering, for example:
* `distinct` setting is not supported for filters
* annotations are not supported, as well


## Development

1. Python 3.8+
0. Install dependencies `pip install poetry && poetry install`

## Testing

1. Python 3.8+
0. Install dependencies `pip install poetry && poetry install`

Check code style: `poetry run flake8`
Run tests: `poetry run pytest`

Tests reports are generated in `tests/reports`.
* `out.xml` - JUnit test results
* `coverage.xml` - Coverage xml results

To generate HTML coverage reports use:
`--cov-report html:tests/reports/cov_html`

## License

`Django Mongoengine RQL` is released under the [Apache License Version 2.0](https://www.apache.org/licenses/LICENSE-2.0).
