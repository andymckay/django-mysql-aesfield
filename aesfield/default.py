from django.conf import settings


def lookup(key=None):
    keys = settings.AES_KEYS
    key = 'default' if not key else key
    if key not in keys:
        raise ValueError('Key %s not found.' % key)

    with open(settings.AES_KEYS[key]) as fp:
        return fp.read()
