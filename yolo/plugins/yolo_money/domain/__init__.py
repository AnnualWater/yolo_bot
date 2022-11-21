# -*- coding: utf-8 -*-
# @Author:归年丶似水
# @Email:2448955276@qq.com
# @GitHub:github.com/AnnualWater

from sqlalchemy import *

from yolo.plugins.db_sqlalchemy import Base


class UserSignInfo(Base):
    __tablename__ = "user_sign_info"
    # 用户ID
    user_id = Column(BIGINT, primary_key=True)
    # 当前金钱
    money = Column(Integer)
    # 最后签到日期
    last_sign = Column(DATETIME)
    # 连续签到天数
    continuous_sign = Column(Integer)

    def __repr__(self):
        return f"UserSignInfo(id={self.id!r})"


Base.metadata.create_all()
