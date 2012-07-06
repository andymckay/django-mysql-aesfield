import os
import base64
from optparse import make_option

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError


def generate_key(byte_length):
    """
    Return a true random ascii string that is byte_length long.
    The resulting key is suitable for cryptogrpahy.
    """
    if byte_length < 32:
        raise ValueError('um, %s is probably not long enough for cryptography'
                         % byte_length)
    key = os.urandom(byte_length)
    key = base64.b64encode(key).rstrip('=')
    key = key[0:byte_length]
    return key


class Command(BaseCommand):
    help = 'Generate a randomized encryption encryption key'
    option_list = BaseCommand.option_list + (
        make_option('--length', action='store', type=int,
                    help='Key length in bytes. Default: %default',
                    default=128),
    )

    def handle(self, *args, **options):
        for dest in settings.AES_KEYS.values():
            if os.path.exists(dest):
                raise CommandError('Key file already exists at %s; remove it '
                                   'first or specify a new path with --dest'
                                   % dest)

        for dest in settings.AES_KEYS.values():
            with open(dest, 'wb') as fp:
                fp.write(generate_key(options['length']))
            os.chmod(dest, 0600)
            print 'Wrote new key: %s' % dest

