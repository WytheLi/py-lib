# 安装一个requests模块
FROM python:alpine3.6
# 安装支持http/https协议客户端请求的库
RUN pip install requests &&\
    pip install aiohttp &&\
    pip install tornado &&\
    pip install selenium &&\
    pip install appium-python-client

# 安装gcc编译环境
# apt-get install
RUN apk add --no-cache gcc musl-dev

# 下列模块的安装需要gcc编译环境
RUN pip install twisted &&\
    pip install gevent

# 安装scrapy
# ubuntu下依赖：libxml2-dev libxslt1-dev zlib1g-dev libffi-dev libssl-dev
RUN apk add --no-cache libxml2-dev libxslt-dev zlib-dev libffi-dev openssl-dev &&\
    pip install scrapy

# 安装pyspider
# ubuntu下的依赖：libcurl4-openssl-dev libxml2-dev libxslt1-dev libssl-dev zlib1g-dev
RUN apk add --no-cache curl-dev openssl-dev libxml2-dev libxslt-dev zlib-dev &&\
    pip install pyspider
    
RUN pip install websocket-client
