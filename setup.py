#!/usr/bin/env python
# encoding=utf-8


import re

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

__author__ = 'xlzd'


def read_version():
    with open('xtls/__init__.py', 'r') as v_file:
        version = re.findall(ur'__version__ = (.+)', v_file.read())[0].decode('utf-8')
        if not version:
            raise RuntimeError("Find version information failed.")
        return version


with open('README.rst', 'rb') as f_readme:
    README = f_readme.read().decode('utf-8')

PACKAGES = ['xtls']

VERSION = read_version()

setup(
    name='xtls',
    version=VERSION,
    keywords=['xlzd', 'python', 'python tools'],
    description=u'xtls: tools just for xlzd',
    long_description=README,
    author='xlzd',
    author_email='i@xlzd.me',
    license='GPLv2',
    url='https://github.com/xlzd/xtls',
    download_url='https://github.com/xlzd/xtls',
    install_requires=[],
    extras_require={},
    packages=PACKAGES,
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: GPLv2 License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)