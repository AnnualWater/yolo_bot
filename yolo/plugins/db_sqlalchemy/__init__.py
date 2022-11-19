# -*- coding: utf-8 -*-
# @Author:归年丶似水
# @Email:2448955276@qq.com
# @GitHub:github.com/AnnualWater

import os

from nonebot import get_driver
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

global_config = get_driver().config
db_url = os.path.abspath(global_config.db_url)
engine = create_engine(f"sqlite:///{db_url}")
Base = declarative_base(engine)


def get_session():
    return sessionmaker(engine)()
