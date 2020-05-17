#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author  : willi
# @Email   : willi168@163.com
# @Description: 优先级队列 权重
import pickle

from .base import BaseRedisQueue
from redis_lock.redis_lock import RedisLock


class PriorityRedisQueue(BaseRedisQueue):
    """利用reids的有序集合实现"""

    def __init__(self, name, host='localhost', port=6379, db=0,
                 maxsize=0, lazy_limit=True, password=None, cluster_nodes=None, redis_lock_config={}):
        super(PriorityRedisQueue, self).__init__(name, host, port, db, maxsize, lazy_limit, password, cluster_nodes)

        self.redis_lock_config = redis_lock_config
        self.lock = None

    def qsize(self):
        self.last_qsize = self.redis.zcard(self.name)
        return self.last_qsize

    def put_nowait(self, obj):
        """

        :param obj: (score, value)
        :return:
        """
        if self.lazy_limit and self.last_qsize < self.maxsize:
            pass
        elif self.full():
            raise self.Full
        # 以下为python与redis旧版本交互参数 新版本报错 AttributeError: ‘int’ object has no attribute ‘items’
        # self.last_qsize = self.redis.zadd(self.name, obj[0], pickle.dumps(obj[1]))
        self.last_qsize = self.redis.zadd(self.name, {pickle.dumps(obj[1]):obj[0]})
        return True

    def get_nowait(self):
        """
        zrange、zrem需要作为一个原子性任务操作
        由于redis的事务并不能保障
        所以此处使用redis分布式锁解决
        :return:
        """
        if not self.lock:
            self.lock = RedisLock(**self.redis_lock_config)

        if self.lock.acquire_lock():
            # ret = self.redis.zrange(self.name, 0, 0)        # 取权重最小的值
            ret = self.redis.zrange(self.name, -1, -1)      # 取权重最大的值
            # print(ret)
            if not ret:
                raise self.Empty
            self.redis.zrem(self.name, ret[0])
            self.lock.release_lock()
            return pickle.loads(ret[0])
