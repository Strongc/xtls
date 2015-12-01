#!/usr/bin/env python
# -*- coding:utf-8 -*-
import sys

reload(sys)
sys.setdefaultencoding("utf-8")


class ConsumerFatalError(Exception):
    """
    当分布式爬虫遇到无法后续任务的异常时，抛出这个异常以停止分配后续任务
    """
    pass


class ProducerFatalError(Exception):
    """
    当分布式爬虫的任务分配遇到无法后续分配的异常时，抛出这个异常以停止后续的操作
    """
    pass


class TimeoutError(Exception):
    """
    当@timeout超时时抛出
    """
    pass
