#!/usr/bin/env python
# encoding=utf-8

"""
descprition
"""

__author__ = 'xlzd'


WORD_DICT = {}


with open(__file__[:__file__.rfind('/')] + '/pinyindata.py', 'r') as f:
    for f_line in f:
        try:
            line = f_line.split('    ')
            WORD_DICT[line[0]] = line[1]
        except:
            line = f_line.split('   ')
            WORD_DICT[line[0]] = line[1]


def _parse_letter(char, only_first):
    letter = WORD_DICT.get('%X' % ord(char), char).split()[0]
    return (letter[:-1], letter[0])[only_first], letter[-1]


def parse(string, only_first=False):
    if not isinstance(string, unicode):
        string = string.decode('utf-8')

    return [_parse_letter(char, only_first) for char in string]


if __name__ == '__main__':
    print parse(u'程度')
