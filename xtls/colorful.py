#!/usr/bin/env python
# encoding=utf-8

__all__ = ['Color', 'dyeing', 'colorful_print']

fmt = u'\033[0;3{}m{}\033[0m'.format


class Color(object):
    BLACK  = 0  # 黑
    RED    = 1  # 红
    GREEN  = 2  # 绿
    YELLOW = 3  # 棕
    BLUE   = 4  # 蓝
    PURPLE = 5  # 紫
    CYAN   = 6  # 青
    GRAY   = 7  # 灰


def dyeing(string, color):
    if not isinstance(string, basestring):
        raise ValueError('string must be a str or unicode, got %s' % type(string))
    if isinstance(string, str):
        string = string.decode('utf-8')
    return fmt(color, string)


def colorful_print(string, color):
    print dyeing(string, color)


if __name__ == '__main__':
    print dyeing('呵呵', Color.YELLOW)
    colorful_print('what', Color.RED)
