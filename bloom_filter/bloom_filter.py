#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author  : willi
# @Email   : willi168@163.com
# @Time    : 20-2-10 上午12:09
# @Description:
import hashlib
import six
import redis


class MultipleHash(object):
    """根据提供的原始数据， salts(加盐), 生成多个hash值"""
    def __init__(self, hash_func_name="md5", salts=["a", "b", "c", "d"]):
        self.hash_func = getattr(hashlib, hash_func_name)
        self.salts = salts  # 初始化一个加盐规则

    def _safe_data(self, data):
        """
        格式化data
        将data转换二进制格式输出
        :param data:
        :return:
        """
        # python3、python2版本兼容
        if six.PY3:
            if isinstance(data, bytes):
                return data
            elif isinstance(data, str):
                return data.encode()
            else:
                raise Exception("data type error, is string or bytes")
        else:
            if isinstance(data, str):
                return data
            elif isinstance(data, unicode):
                return data.encode()
            else:
                raise Exception("data type error, is string or bytes")

    def get_hash_values(self, data):
        hash_val_list = []
        for salt in self.salts:
            hash_obj = self.hash_func()
            hash_obj.update(self._safe_data(data))
            hash_obj.update(self._safe_data(salt))  # 加盐
            hash_value = hash_obj.hexdigest()
            hash_val_list.append(int(hash_value, 16))
        return hash_val_list


class BloomFilter(object):
    """布隆去重"""
    def __init__(self, redis_host="localhost", redis_port=6379, redis_db=0, hash_table_name="hash_table"):
        self.redis_host = redis_host
        self.redis_port = redis_port
        self.redis_db = redis_db
        self.hash_table_name = hash_table_name  # redis中构造hash表
        self.pool = redis.ConnectionPool(host=self.redis_host, port=self.redis_port, db=self.redis_db)
        self.client = redis.StrictRedis(connection_pool=self.pool)
        self.multiple_hash = MultipleHash()

    def _get_offset(self, hash_value):
        """
        获取偏移量
        redis String值最大512M
        :param hash_value:
        :return:
        """
        return hash_value % (512 * 1024 * 1024 * 8)

    def save(self, data):
        """
        向hash表指定二进制位设置1
        :param data: 原始数据
        :return: True
        """
        hash_val_list = self.multiple_hash.get_hash_values(data)
        for hash_value in hash_val_list:
            offset = self._get_offset(hash_value)
            self.client.setbit(self.hash_table_name, offset, 1)
        return True

    def is_exists(self, data):
        """
        判断指定偏移量二进制位等于0
        :param data: 原始数据
        :return: True or False
        """
        hash_val_list = self.multiple_hash.get_hash_values(data)
        for hash_value in hash_val_list:
            offset = self._get_offset(hash_value)
            res = self.client.getbit(self.hash_table_name, offset)
            if res == 0:
                return False
        return True


if __name__ == "__main__":
    bloom_filter = BloomFilter(redis_host="172.17.0.4")
    test_data = ["aaa", "111", "bbb", "abc", "aaa"]
    for data in test_data:
        res = bloom_filter.is_exists(data)
        print(res, data)
        if not res:
            bloom_filter.save(data)

