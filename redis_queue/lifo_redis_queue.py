#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author  : willi
# @Email   : willi168@163.com
# @Description:
import pickle

from .base import BaseRedisQueue


class LifoRedisQueue(BaseRedisQueue):
    def get_nowait(self):
        ret = self.redis.rpop(self.name)
        if not ret:
            raise self.Empty
        return pickle.loads(ret)
