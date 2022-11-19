# -*- coding: utf-8 -*-
# @Author:归年丶似水
# @Email:2448955276@qq.com
# @GitHub:github.com/AnnualWater

from sqlalchemy import *

from yolo.plugins.db_sqlalchemy import Base


class CustomReplyDbItem(Base):
    __tablename__ = "custom_reply"
    id = Column(Integer, primary_key=True)

    create_user_id = Column(Integer)
    group_id = Column(Integer)

    # 回复消息
    message = Column(String(200))
    # 指令
    command = Column(String(200))
    # 指令是否启用正则
    is_regex = Column(Boolean)
    # 回复类型 private group group_private
    response_type = Column(String)

    def __repr__(self):
        return f"CustomReply(id={self.id!r})"


Base.metadata.create_all()
