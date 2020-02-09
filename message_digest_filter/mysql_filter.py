#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author  : willi
# @Email   : willi168@163.com
# @Time    : 20-2-7 上午9:39
# @Description:
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from . import BaseFilter

Base = declarative_base()


# class Signature(Base):
#     """存储指纹的模型类"""
#     __tablename__ = "signature"
#
#     id = Column(Integer, primary_key=True, autoincrement=True)
#     hash_value = Column(String(80), index=True, unique=True)


class MysqlFilter(BaseFilter):
    def __init__(self, hash_func_name="md5", mysql_url=None, table_name="signature"):
        super(MysqlFilter, self).__init__(hash_func_name)

        # # 动态的创建模型类
        # class Signature(Base):
        #     """存储指纹的模型类"""
        #     __tablename__ = table_name
        #
        #     id = Column(Integer, primary_key=True, autoincrement=True)
        #     hash_value = Column(String(80), index=True, unique=True)
        #
        # self.table = Signature

        # 利用type() 超类 创建类
        self.table = type("Signature", (Base,), dict(
            __tablename__=table_name,
            id=Column(Integer, primary_key=True, autoincrement=True),
            hash_value=Column(String(80), index=True, unique=True)
        ))

        self.engine = create_engine(mysql_url)
        Base.metadata.create_all(self.engine)  # 根据模型类创建表格，表存在则忽略
        self.Session = sessionmaker(self.engine)

    def _save(self, hash_value):
        session = self.Session()
        sign = self.table(hash_value=hash_value)
        session.add(sign)
        session.commit()
        session.close()

    def _is_exists(self, hash_value):
        session = self.Session()
        sign = session.query(self.table).filter_by(hash_value=hash_value).first()
        session.close()
        if sign:
            return True
        return False
