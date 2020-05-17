#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author  : willi
# @Email   : willi168@163.com
# @Description:
from lib.redis_queue.priority_redis_queue import PriorityRedisQueue

pqueue = PriorityRedisQueue('pqueue', db=15, redis_lock_config={'lock_name': 'distributed_lock'})

print(pqueue.put((100, 'value3')))
print(pqueue.get(block=False))
