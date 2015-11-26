#!/usr/bin/env python
# -*- coding:utf-8 -*-
import sys

from codehelper import singleton

reload(sys)
sys.setdefaultencoding("utf-8")

_DEFAULT_CONTACT_POINTS = ['127.0.0.1']


@singleton
class CassandraProxy(object):
    def __init__(self, contact_points=_DEFAULT_CONTACT_POINTS, port=9042):
        from cassandra.cluster import Cluster
        self._cluster = Cluster(contact_points, port)
        self._sessions = {}

    def _get_session(self, keyspace):
        if keyspace not in self._sessions:
            self._sessions[keyspace] = self._cluster.connect(keyspace)
        return self._sessions[keyspace]

    def _build(self, value):
        if isinstance(value, list):
            return '({items})'.format(items=','.join([self._build(i) for i in value]))
        return ("%s", "'%s'")[isinstance(value, basestring)] % value

    def _run(self, keyspace, cql):
        return self._get_session(keyspace).execute(query=cql)

    def select(self, keyspace, table, select_items=None, filter_dict=None, limit=None):
        """
        从cassandra中查找
        :param select_items: 需要搜索的项（不填写即为所有）
        :param filter_dict: 查询条件
        :param limit: 返回前多少条
        :return: list<cassandra.io.asyncorereactor.Row>
        """
        if not select_items:
            select_items = ['*']
        if not isinstance(select_items, list):
            raise ValueError('select items must be a list, got %s' % type(select_items))
        cql = 'SELECT %s FROM %s' % (','.join(select_items), table)
        if isinstance(filter_dict, dict) and filter_dict:
            cql += ' WHERE ' + ' and '.join(['{k}%s{v}'.format(k=k, v=self._build(v)) % ('=', ' in ')[isinstance(v, list)] for (k,v) in filter_dict.iteritems()])
        if isinstance(limit, int):
            cql = cql + ' LIMIT %d' % limit
        return self._run(keyspace, cql)

    def insert(self, keyspace, table, data, filter=None):
        """
        插入数据
        :param data: 需要插入的数据（dict）
        :param filter: 如果为None则对data全部插入，如果需要挑选某些字段则制定一个filter（接受一个参数并返回bool）
        """
        if not isinstance(data, dict):
            raise ValueError('data must be a dict, got %s' % type(data))
        if not filter:
            filter = lambda _: True
        data = [(k, v) for k, v in data.iteritems() if filter(k)]
        fields = ', '.join((item[0] for item in data))
        values = ', '.join((self._build(item[1]) for item in data))
        cql = 'INSERT INTO {table} ({fields}) VALUES ({values})'.format(table=table, fields=fields, values=values)
        self._run(keyspace, cql)

    def delete(self, keyspace, table, condition):
        """
        删除数据
        :param condition: 删除的条件(dict)
        """
        if not isinstance(condition, dict):
            raise ValueError('condition must be a dict, got %s' % type(data))
        if not condition:
            raise ValueError('condition is None')
        condition = ' and '.join('%s=%s' % (k, self._build(v)) for (k, v) in condition.iteritems())
        cql = "DELETE from {table} WHERE {condition}".format(table=table, condition=condition)
        return self._run(keyspace, cql)


if __name__ == '__main__':
    CASSANDRA = CassandraProxy(['192.168.31.48'])
    # x = CASSANDRA._get_session('crawler')
    # for xx in x.execute(query="SELECT * FROM news_by_key WHERE period in (201511,201111) and key='杭州誉存科技有限公司'"):
    #     print xx
    for xx in CASSANDRA.select('crawler', 'news_by_key', filter_dict={'key': u'杭州誉存科技有限公司', 'period': [201511, 201111]}):
        print xx
