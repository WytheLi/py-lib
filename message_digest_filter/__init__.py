#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author  : willi
# @Email   : willi168@163.com
# @Time    : 20-2-7 上午9:39
# @Description: 信息摘要hash算法（指纹算法）
import hashlib
import six


class BaseFilter(object):

    def __init__(self, hash_func_name='md5'):
        self.hash_func = getattr(hashlib, hash_func_name)   # 根据对象属性/方法名，获取对应属性/方法对象

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

    def _get_hash_value(self, data):
        """
        生成data数据对应的指纹
        :param data:
        :return:
        """
        # # md5
        # md5 = hashlib.md5()
        # md5.update(data)
        # hash_value = md5.hexdigest()
        # # sha1
        # sha1 = hashlib.sha1()
        # sha1.update(data)
        # hash_value = sha1.hexdigest()
        hash_obj = self.hash_func()
        hash_obj.update(self._safe_data(data))
        hash_value = hash_obj.hexdigest()
        return hash_value

    def _is_exists(self, hash_value):
        """
        提供给子类重写，判断指纹是否在内存/或数据库中已经存在
        :param hash_value:
        :return:
        """
        pass

    def _save(self, hash_value):
        """
        提供给子类重写，保存指纹到内存/数据库中，并返回存储结果
        :param hash_value:
        :return:
        """
        pass

    def sava(self, data):
        """
        根据data计算出对应的指纹进行存储
        :param data: 原始数据
        :return: 存储结果
        """
        hash_value = self._get_hash_value(data)
        return self._save(hash_value)

    def is_exists(self, data):
        """
        判断data数据对应的指纹是否存在
        :param data: 原始数据
        :return: True or False
        """
        hash_value = self._get_hash_value(data)
        return self._is_exists(hash_value)
