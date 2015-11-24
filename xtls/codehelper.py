#!/usr/bin/env python
# -*- coding:utf-8 -*-
import os
import sys
import time
import getpass
import socket
import fcntl
import struct
import traceback
from functools import wraps

from timeparser import now

reload(sys)
sys.setdefaultencoding("utf-8")

__all__ = [
    'timeit',
    'no_exception',
    'get_user',
    'get_ip',
    'get_runner',
    'singleton'
]


def timeit(argument):
    """
    检测函数运行时间的装饰器
    支持不传参数的写法：
        @timeit
        def func(): pass
    或者传入一个logger：
        @timeit(logger)
        def func(): pass
    空参情况下将会打印运行时间到控制台，传入logger则会通过logger处理。
    """
    if hasattr(argument, 'info'):
        def decorator(function):
            @wraps(function)
            def wrapper(*args, **kwargs):
                start_time = time.time()
                argument.info('function [%s] start at [%s]' % (function.__name__, now(obj=False, precise=True)))
                rst = function(*args, **kwargs)
                argument.info('function [%s] exit  at [%s]' % (function.__name__, now(obj=False, precise=True)))
                argument.info('function [%s] coast [%sms]' % (function.__name__, (time.time() - start_time)*1000))
                return rst
            return wrapper
        return decorator
    if callable(argument):
        @wraps(argument)
        def wrapper(*args, **kwargs):
            start_time = time.time()
            print 'function [%s] start at [%s]' % (argument.__name__, now(obj=False, precise=True))
            rst = argument(*args, **kwargs)
            print 'function [%s] exit  at [%s]' % (argument.__name__, now(obj=False, precise=True))
            print 'function [%s] coast [%sms]' % (argument.__name__, (time.time() - start_time)*1000)
            return rst
        return wrapper
    raise ValueError('argument error.')


def no_exception(on_exception, logger=None):
    """
    处理函数抛出异常的装饰器， ATT: on_exception必填
    :param on_exception: 遇到异常时函数返回什么内容
    """
    def decorator(function):
        def wrapper(*args, **kwargs):
            try:
                result = function(*args, **kwargs)
            except Exception, e:
                if hasattr(logger, 'exception'):
                    logger.exception(e)
                else:
                    print traceback.format_exc()
                result = on_exception
            return result
        return wrapper
    return decorator


def get_user():
    """
    获取运行程序的用户名
    :return:
    """
    try:
        return os.getlogin()
    except:
        return getpass.getuser()


def get_ip():
    """
    获取本机IP
    """
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # 0x8915 -> SIOCGIFADDR
    try:
        return socket.inet_ntoa(fcntl.ioctl(s.fileno(), 0x8915, struct.pack('256s', 'eth1'))[20:24])
    except Exception, e:
        try:
            return socket.inet_ntoa(fcntl.ioctl(s.fileno(), 0x8915, struct.pack('256s', 'wlan0'))[20:24])
        except Exception, e:
            try:
                return socket.inet_ntoa(fcntl.ioctl(s.fileno(), 0x8915, struct.pack('256s', 'eth0'))[20:24])
            except Exception, e:
                return socket.gethostbyname(socket.getfqdn(socket.gethostname()))


def get_runner():
    """
    获取运行程序的用户名和当前机器的IP
    """
    return '%s@%s' % (get_user(), get_ip())


def singleton(cls):
    """
    单例模式的装饰器： 在需要单例的类定义上加 @singleton 即可
    """
    INSTANCES = {}

    def _singleton(*args, **kwargs):
        if cls not in INSTANCES:
            INSTANCES[cls] = cls(*args, **kwargs)
        return INSTANCES[cls]
    return _singleton


if __name__ == '__main__':
    print get_ip()
