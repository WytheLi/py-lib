#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author  : willi
# @Email   : willi168@163.com
# @Description: redis分布式锁
import time
import threading
import socket
import os
import redis


class RedisLock(object):
    def __init__(self, lock_name, host='localhost', port=6379, db=0, password=None):
        self.redis = redis.StrictRedis(host=host, port=port, db=db, password=password)
        self.lock_name = lock_name

    def acquire_lock(self, thread_id=None, expire=1, block=True):
        """
        上锁
        :param thread_id:
        :param expire: 锁的有效期  防止程序意外中断，未被程序主动解锁，造成死锁
        :param block: 阻塞
        :return:
        """
        if not thread_id:
            thread_id = socket.gethostname() + '-' + str(os.getpid()) + '-' + str(threading.current_thread().ident)
        while block:
            # 存在值(设置失败)返回False， 否则返回True
            ret = self.redis.setnx(self.lock_name, thread_id)
            if ret:
                self.redis.expire(self.lock_name, expire)
                return True
            time.sleep(0.001)   # 避免因循环执行过快，对cup的过载

        ret = self.redis.setnx(self.lock_name, thread_id)
        if ret:
            self.redis.expire(self.lock_name, expire)
            return True
        else:
            return False

    def release_lock(self, thread_id=None):
        """
        解锁
        :param thread_id:
        :return:
        """
        if not thread_id:
            thread_id = socket.gethostname() + '-' + str(os.getpid()) + '-' + str(threading.current_thread().ident)

        ret = self.redis.get(self.lock_name)
        if not ret and ret.decode() == thread_id:
            self.redis.delete(self.lock_name)
            return True
        else:
            return False


if __name__ == '__main__':
    lock = RedisLock("distributed_lock")

    # thread_id = '服务器' + '进程号' + thread_id
    _hostname = socket.gethostname()
    _pid = str(os.getpid())
    _tid = str(threading.current_thread().ident)
    thread_id = _hostname + "-" + _pid + "-" + _tid
    if lock.acquire_lock(thread_id, expire=3):
        print("执行多个任务操作，将这些任务当成一个原子性任务...")
        # lock.release_lock(thread_id)
