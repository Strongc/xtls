#!/usr/bin/env python
# -*- coding:utf-8 -*-
import sys
import urllib
import hashlib

from bs4 import BeautifulSoup as _beautifulsoup

reload(sys)
sys.setdefaultencoding("utf-8")

try:
    __import__('lxml')
    BeautifulSoup = lambda markup, from_encoding=None: _beautifulsoup(markup, 'lxml', from_encoding=from_encoding)
except ImportError:
    try:
        __import__('html5lib')
        BeautifulSoup = lambda markup, from_encoding=None: _beautifulsoup(markup, 'html5lib', from_encoding=from_encoding)
    except ImportError:
        BeautifulSoup = lambda markup, from_encoding=None: _beautifulsoup(markup, 'html.parser', from_encoding=from_encoding)


def url_encode(string, encoding='utf-8'):
    if isinstance(string, unicode):
        string = string.encode(encoding)
    return urllib.quote(string)


def url_decode(string, encoding='utf-8'):
    return urllib.unquote(string).decode(encoding)


def to_str(obj):
    """
    convert a object to string
    """
    if isinstance(obj, str):
        return obj
    if isinstance(obj, unicode):
        return obj.encode('utf-8')
    return str(obj)


def to_unicode(obj):
    """
    convert a object to unicode string
    """
    return obj.decode('utf-8')

_gen_digest = lambda algo: getattr(hashlib, algo)

md5 = lambda data: _gen_digest('md5')(data).hexdigest()
sha1 = lambda data: _gen_digest('sha1')(data).hexdigest()
sha224 = lambda data: _gen_digest('sha224')(data).hexdigest()
sha256 = lambda data: _gen_digest('sha256')(data).hexdigest()
sha384 = lambda data: _gen_digest('sha384')(data).hexdigest()
sha512 = lambda data: _gen_digest('sha512')(data).hexdigest()


if __name__ == '__main__':
    print sha512('abc')

