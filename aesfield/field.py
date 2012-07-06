from django.db import models
from django.db import connection
from django.utils.importlib import import_module


class EncryptedField(Exception):
    pass


class AESField(models.CharField):

    description = 'A field that uses MySQL AES encryption.'
    __metaclass__ = models.SubfieldBase

    def __init__(self, *args, **kwargs):
        super(AESField, self).__init__(*args, **kwargs)
        self.aes_prefix = kwargs.get('aes_prefix', 'aes:')
        if not self.aes_prefix:
            raise ValueError('AES Prefix cannot be null.')
        self.aes_method = kwargs.get('aes_method', 'aesfield.default')
        if not self.aes_method:
            raise ValueError('AES Method cannot be null.')
        self.aes_key = kwargs.get('aes_key', '')

    def get_aes_key(self):
        result = import_module(self.aes_method).lookup(self.aes_key)
        if len(result) < 10:
            raise ValueError('Passphrase cannot be less than 10 chars.')
        return result

    def get_prep_lookup(self, type, value):
        raise EncryptedField('You cannot do lookups on an encrypted field.')

    def get_db_prep_lookup(self, *args, **kw):
        raise EncryptedField('You cannot do lookups on an encrypted field.')

    def get_db_prep_value(self, value, connection, prepared=False):
        if not prepared:
            cursor = connection.cursor()
            cursor.execute('SELECT CONCAT(%s, HEX(AES_ENCRYPT(%s, %s)))',
                           (self.aes_prefix, value, self.get_aes_key()))
            value = cursor.fetchone()[0]
        return value

    def to_python(self, value):
        if not value.startswith('aes:'):
            return value
        cursor = connection.cursor()
        cursor.execute('SELECT AES_DECRYPT(UNHEX(SUBSTRING(%s, %s)), %s)',
                       (value, len(self.aes_prefix) + 1, self.get_aes_key()))
        res = cursor.fetchone()[0]
        if res:
            value = res
        return value
