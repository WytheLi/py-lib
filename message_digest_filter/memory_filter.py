#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author  : willi
# @Email   : willi168@163.com
# @Time    : 20-2-7 上午9:39
# @Description: 利用内存 set()容器去重
from . import BaseFilter


class MemoryFilter(BaseFilter):
    def __init__(self, hash_func_name="md5"):
        super(MemoryFilter, self).__init__(hash_func_name)
        # print(self.hash_func)
        self.storage = set()

    def _save(self, hash_value):
        """

        :param hash_value:
        :return: 存储结果
        """
        return self.storage.add(hash_value)

    def _is_exists(self, hash_value):
        if hash_value in self.storage:
            return True
        else:
            return False
