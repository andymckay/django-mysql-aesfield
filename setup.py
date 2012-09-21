import os
from setuptools import setup


setup(
    name='django-mysql-aesfield',
    version='0.2',
    description='Django Model Field that supports AES encryption in MySQL',
    long_description=open('README.rst').read(),
    author='Andy McKay',
    author_email='andym@mozilla.com',
    license='BSD',
    url='https://github.com/andymckay/django-mysql-aesfield',
    include_package_data=True,
    zip_safe=False,
    classifiers=[
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Framework :: Django'
        ],
    )
