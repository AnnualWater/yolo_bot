# -*- coding: utf-8 -*-
# @Author:归年丶似水
# @Email:2448955276@qq.com
# @GitHub:github.com/AnnualWater

from sqlalchemy import *

from yolo.plugins.db_sqlalchemy import Base


class ComicSubscriptionInfo(Base):
    __tablename__ = "comic_subscription"
    id = Column(Integer, primary_key=True)
    create_user_id = Column(Integer)
    group_id = Column(Integer)

    # 番剧ID
    comic_id = Column(String)
    # 番剧名
    title = Column(String)
    # 平台
    platform = Column(String)
    # 当前追到的集数
    episode = Column(String)
    # 更新信息
    update_info = Column(String)
    # 订阅类型
    scheduled_type = Column(String)

    def __repr__(self):
        return f"ComicSubscriptionInfo(id={self.id!r})"


Base.metadata.create_all()
