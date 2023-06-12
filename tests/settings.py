import os


INSTALLED_APPS = [
    'django_mongoengine',
]

MONGODB_DATABASES = {
    'default': {
        'name': 'mongoenginetest',
        'host': os.environ.get('MONGO_HOST', 'mongomock://localhost'),
        'username': os.environ.get('MONGO_USER'),
        'password': os.environ.get('MONGO_PASSWORD'),
    },
}
