#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author  : li
# @Email   : wytheli168@163.com
# @Time    : 20-2-7 上午9:39
# @Description: 利用redis数据库去重
import redis
from . import BaseFilter


class RedisFilter(BaseFilter):
    def __init__(self, hash_func_name="md5", redis_host="localhost", redis_port=6379, redis_db=0, redis_filter_key="filter_set"):
        super(RedisFilter, self).__init__(hash_func_name)
        self.redis_filter_key = redis_filter_key
        self.pool = redis.ConnectionPool(host=redis_host, port=redis_port, db=redis_db)
        self.client = redis.StrictRedis(connection_pool=self.pool)

    def _save(self, hash_value):
        return self.client.sadd(self.redis_filter_key, hash_value)

    def _is_exists(self, hash_value):
        return self.client.sismember(self.redis_filter_key, hash_value)
