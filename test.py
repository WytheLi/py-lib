#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author  : willi
# @Email   : willi168@163.com
# @Time    : 20-2-7 上午11:40
# @Description:
import sys

from message_digest_filter.memory_filter import MemoryFilter
from message_digest_filter.mysql_filter import MysqlFilter

test_data = ["aaa", "111", "aaa", "ccc", "担当", "111"]
# print(sys.path)

# 使用mysql去重
# mysql_url = "mysql+pymysql://username:password@localhost:3306/db_name"
mysql_url = "mysql+pymysql://root:password@172.17.0.2:3306/filter"
filter = MysqlFilter(mysql_url=mysql_url, table_name="sign")

# 内存去重
# filter = MemoryFilter()

for data in test_data:
    print(data, filter.is_exists(data))
    if not filter.is_exists(data):
        filter.sava(data)
# print(filter.storage)

