#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author  : willi
# @Email   : willi168@163.com
# @Description: 修改自scrapy redis_queue

import time
import pickle

import redis
# import umsgpack     # 序列化/反序列化
from six.moves import queue as BaseQueue


class BaseRedisQueue(object):
    """
    A Queue like message built over redis
    """

    Empty = BaseQueue.Empty
    Full = BaseQueue.Full
    max_timeout = 0.3

    def __init__(self, name, host='localhost', port=6379, db=0,
                 maxsize=0, lazy_limit=True, password=None, cluster_nodes=None):
        """
        Constructor for RedisQueue

        maxsize:    an integer that sets the upperbound limit on the number of
                    items that can be placed in the queue.
        lazy_limit: redis queue is shared via instance, a lazy size limit is used
                    for better performance.
        """
        self.name = name
        if (cluster_nodes is not None):
            from rediscluster import StrictRedisCluster
            # cluster_nodes = [
            #     {'host': '172.16.179.131', 'port': '7000'},
            #     {'host': '172.16.179.142', 'port': '7003'},
            #     {'host': '172.16.179.131', 'port': '7001'},
            # ]
            self.redis = StrictRedisCluster(startup_nodes=cluster_nodes)  # redis集群交互 startup_nodes为集群节点的配置
        else:
            self.redis = redis.StrictRedis(host=host, port=port, db=db, password=password)
        self.maxsize = maxsize
        self.lazy_limit = lazy_limit
        self.last_qsize = 0

    def qsize(self):
        self.last_qsize = self.redis.llen(self.name)
        return self.last_qsize

    def empty(self):
        if self.qsize() == 0:
            return True
        else:
            return False

    def full(self):
        if self.maxsize and self.qsize() >= self.maxsize:
            return True
        else:
            return False

    def put_nowait(self, obj):
        if self.lazy_limit and self.last_qsize < self.maxsize:
            pass
        elif self.full():
            raise self.Full
        # self.last_qsize = self.redis.rpush(self.name, umsgpack.packb(obj))      # umsgpack.packb()将对象序列化为二进制字符串
        self.last_qsize = self.redis.rpush(self.name, pickle.dumps(obj))
        return True

    def put(self, obj, block=True, timeout=None):
        if not block:
            return self.put_nowait(obj)

        start_time = time.time()
        while True:
            try:
                return self.put_nowait(obj)
            except self.Full:
                if timeout:
                    lasted = time.time() - start_time
                    if timeout > lasted:
                        time.sleep(min(self.max_timeout, timeout - lasted))
                    else:
                        raise
                else:
                    time.sleep(self.max_timeout)

    def get_nowait(self):
        ret = self.redis.lpop(self.name)
        if ret is None:
            raise self.Empty
        # return umsgpack.unpackb(ret)    # umsgpack.unpackb()将二进制文件反序列化为python类型
        return pickle.loads(ret)

    def get(self, block=True, timeout=None):
        if not block:
            return self.get_nowait()

        start_time = time.time()
        while True:
            try:
                return self.get_nowait()
            except self.Empty:
                if timeout:
                    lasted = time.time() - start_time
                    if timeout > lasted:
                        time.sleep(min(self.max_timeout, timeout - lasted))
                    else:
                        raise
                else:
                    time.sleep(self.max_timeout)
