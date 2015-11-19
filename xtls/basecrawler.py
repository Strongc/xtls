#!/usr/bin/env python
# -*- coding:utf-8 -*-
import sys
import random
from pprint import pprint

import requests


reload(sys)
sys.setdefaultencoding("utf-8")

USER_AGENTS = [
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.90 Safari/537.36'
]


def random_user_agent():
    return random.choice(USER_AGENTS)


class BaseCrawler(object):
    def __init__(self, **kwargs):
        logger = kwargs.get('logger')
        if logger:
            self._log = logger.info
            self._exception = logger.exception
            del kwargs['logger']
        else:
            self._exception = self._log = pprint
        self.__dict__ = dict(self.__dict__, **kwargs)
        self._request = requests.Session()
        self._request.headers['User-Agent'] = random_user_agent()

    def get_raw(self, url, timeout=10, times=3):
        if times == 0:
            return None
        try:
            return self._request.get(url, timeout=timeout)
        except Exception, e:
            self._exception(e)
            return self.get_raw(url, timeout=timeout, times=times - 1)

    def get(self, url, timeout=10, times=3):
        raw = self.get_raw(url, timeout=timeout, times=times)
        if raw:
            return raw.content
        return None

    def post_raw(self, url, data, headers=None, timeout=10, times=3):
        if times == 0:
            return None
        try:
            if headers:
                headers = dict(self._request.headers, **headers)
                return self._request.post(url, data=data, headers=headers, timeout=timeout)
            return self._request.post(url, data=data, timeout=timeout)
        except Exception, e:
            self._exception(e)
            return self.post_raw(url, data, headers=headers, timeout=timeout, times=times - 1)

    def post(self, url, data, headers=None, timeout=10, times=3):
        raw = self.post_raw(url, data, headers=headers, timeout=timeout, times=times)
        if raw:
            return raw.content
        return None
