# 配置基本的python开发环境
FROM python:alpine3.6
RUN apk add --no-cache gcc musl-dev
RUN apk add --no-cache libffi-dev && pip install ipython
RUN apk add --no-cache openssl-dev && pip install redis && pip install pymysql && pip install sqlalchemy && pip install six && pip install w3lib