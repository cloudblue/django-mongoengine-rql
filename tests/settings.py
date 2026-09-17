import os


INSTALLED_APPS = []

MONGODB_DATABASES = {
    'default': {
        'name': 'mongoenginetest',
        'host': os.environ.get('MONGO_HOST'),
        'username': os.environ.get('MONGO_USER'),
        'password': os.environ.get('MONGO_PASSWORD'),
    },
}
