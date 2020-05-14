#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author  : willi
# @Email   : willi168@163.com
# @Description: 优先级队列 权重
import pickle

from .base import BaseRedisQueue


class PriorityRedisQueue(BaseRedisQueue):
    """利用reids的有序集合实现"""
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
        # ret = self.redis.zrange(self.name, 0, 0)        # 取权重最小的值
        ret = self.redis.zrange(self.name, -1, -1)      # 取权重最大的值
        # print(ret)
        if not ret:
            raise self.Empty
        self.redis.zrem(self.name, ret[0])
        return pickle.loads(ret[0])
