#!/usr/bin/env python
# -*- coding:utf-8 -*-
import re
import sys
from pprint import pprint
from functools import wraps
try:
    from cPickle import dumps, loads
except ImportError:
    from pickle import dumps, loads

from errors import ConsumerFatalError, ProducerFatalError
reload(sys)
sys.setdefaultencoding("utf-8")

_deal_uri = lambda uri: uri if re.match(ur'tcp://(.+?):(\d+)', uri) else 'tcp://{host}:61613'.format(host=uri)


def _deal_logger(logger):
    if logger:
        return logger.info, logger.exception
    return pprint, pprint


def _conn(cfg_uri, queue, _info):
    from stompest.config import StompConfig
    from stompest.sync import Stomp

    _info('Init Stomp obj: [%s-%s]' % (cfg_uri, queue))
    client = Stomp(StompConfig(cfg_uri))
    _info('connecting... %s' % cfg_uri)
    client.connect()
    _info('connected %s' % cfg_uri)
    return client


def consumer(cfg_uri, queue, param_type=str, logger=None):
    """
    分布式爬虫的爬虫端（具体爬虫部分）
    被包装的函数必须满足如下要求：
       1. 有且仅有一个参数（参数类型不限，由param_type指定参数类型）
       2. 对于每个任务，返回两个参数： code, message

    :param cfg_uri: 读取任务的路径
    :param queue: Queue的名字
    :param param_type: 所包装的函数接受的参数类型
    :param logger: 日志记录工具
    """
    from stompest.protocol import StompSpec

    _info, _exception = _deal_logger(logger)
    cfg_uri = _deal_uri(cfg_uri)

    def decorator(function):
        @wraps(function)
        def wapper():
            client = _conn(cfg_uri, queue, _info)
            client.subscribe(queue, {StompSpec.ACK_HEADER: StompSpec.ACK_CLIENT_INDIVIDUAL})
            while True:
                try:
                    frame = client.receiveFrame()
                    _info('got new frame %s' % frame)
                    param = loads(frame.body)
                    assert isinstance(param, param_type)
                    code, msg = function(param)
                    _info('result of task [%s]: [%s]-[%s]' % (frame.body, code, msg))
                except (KeyboardInterrupt, AssertionError, ConsumerFatalError), e:
                    _exception(e)
                    break
                except Exception, e:
                    _exception(e)
                finally:
                    try:
                        client.ack(frame)
                    except:
                        pass
            client.disconnect()
            _info('disconnected %s' % cfg_uri)
        return wapper
    return decorator


def producer(cfg_uri, queue, logger=None):
    """
    分布式爬虫的任务端（将任务加入Queue）

    注意：
        被包装的函数需要返回一个可迭代的对象

    :param cfg_uri: 读取任务的路径
    :param queue: Queue的名字
    :param logger: 日志记录工具
    """
    _info, _exception = _deal_logger(logger)
    cfg_uri = _deal_uri(cfg_uri)

    def decorator(function):
        @wraps(function)
        def wapper(*args, **kwargs):
            client = _conn(cfg_uri, queue, _info)
            for item in function(*args, **kwargs):
                try:
                    data = dumps(item)
                    client.send(queue, data, headers={'persistent': 'true'})
                    _info('Producer insert %s - %s' % (queue, item))
                except ProducerFatalError, e:
                    _exception(e)
                    break
                except Exception, e:
                    _exception(e)
            client.disconnect()
            _info('disconnected %s' % cfg_uri)
        return wapper
    return decorator


""" ################ USEAGE #######################
@producer('192.168.31.116', queue='/queue/test')
def _produce(size):
    for x in xrange(size):
        yield {'key': x}


@consumer('192.168.31.116', queue='/queue/test', param_type=str)
def _task(key):
    print key
    print '-' * 120
    return 0, 'msg of task'
"""

if __name__ == '__main__':
    _task()
    # _produce(10)
    # _produ