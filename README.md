### docker搭建python环境
```bash
docker build -f python-dev/Dockerfile .
```

### 拉取redis、mysql镜像
```bash
docker pull mysql:5.7
docker pull redis:alpine
```


### 持久化去重
1. 信息摘要hash算法（指纹）  
    message_digest_filter  
    |-\_\_init__.py  
    |-memory_filter.py  使用内存中的容器去重  
    |-mysql_filter.py  使用mysql数据库去重  
    |-redis_filter.py  使用redis数据库去重
2. SimHash算法（模糊文本去重）  
[python实现的SimHash算法](https://github.com/leonsim/simhash)  
[序列化反序列化](https://segmentfault.com/a/1190000019217718)

3. 布隆过滤  
[Python实现的内存版布隆过滤器pybloom](Python实现的内存版布隆过滤器pybloom)
- 手动实现一个redis版本的bloom过滤器
    - 使用hash算法(md5, sha1, sha128...)，生成多个hash值
    - 使用一个hash算法，对需要处理的数据通过加盐处理，生成多个hash值

### 持久化队列
- 基于文件的队列
    - [queuelib中的disk_queue](https://github.com/scrapy/queuelib)
- 基于redis实现的queue
    - [pyspider中的redis_queue](https://github.com/binux/pyspider/blob/master/pyspider/message_queue/redis_queue.py)
    - 基于redis的FIFO、LIFO、Priority队列  
    redis_queue  
    |- \_\_init\_\_.py  
    |- base.py  
    |- fifo_redis_queue.py  
    |- lifo_redis_queue.py  
    |- priority_redis_queue.py  
    
### redis分布式锁
redis_lock  
|- \_\_init\_\_.py  
|- redis_lock.py




