#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author  : willi
# @Email   : willi168@163.com
# @Description:
from redis_queue.priority_redis_queue import PriorityRedisQueue

pqueue = PriorityRedisQueue('pqueue', db=15)

# pqueue.put((100, 'value1'))
pqueue.get(block=False)
