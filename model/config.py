# -*- coding: utf-8 -*-
import redis as redis
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# 初始化数据库连接:
engine = create_engine('mysql+pymysql://root:root@localhost:3306/spider?charset=utf8mb4')
# 创建DBSession类型:
DBSession = sessionmaker(bind=engine)
# 初始化redis数据库连接
Redis = redis.StrictRedis(host='localhost', port=6379, db=0)
