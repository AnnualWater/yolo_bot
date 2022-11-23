# @Author:归年丶似水
# @Email:2448955276@qq.com
# @GitHub:github.com/AnnualWater

from sqlalchemy import *

from yolo.plugins.db_sqlalchemy import Base


class CrazyKfcGroup(Base):
    __tablename__ = "crazy_kfc_group"
    group_id = Column(Integer, primary_key=True)

    def __repr__(self):
        return f"CrazyKfcGroup(id={self.id!r})"


Base.metadata.create_all()