INSTALLED_APPS = [
    'django_mongoengine',
]

MONGODB_DATABASES = {'default': {
    'name': 'mongoenginetest',
    'host': 'mongomock://localhost',
}}
