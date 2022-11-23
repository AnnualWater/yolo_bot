# -*- coding: utf-8 -*-
# @Author:归年丶似水
# @Email:2448955276@qq.com
# @GitHub:github.com/AnnualWater

from yolo.plugins.crazy_kfc.domain import CrazyKfcGroup
from yolo.plugins.db_sqlalchemy import get_session


def add_group(group_id: int):
    session = get_session()
    group = session.query(CrazyKfcGroup).get(group_id)
    if group is None:
        session.add(CrazyKfcGroup(group_id=group_id))
        session.commit()
    session.close()


def del_group(group_id: int):
    session = get_session()
    group = session.query(CrazyKfcGroup).get(group_id)
    if group is not None:
        session.delete(group)
        session.commit()
    session.close()


def get_groups():
    session = get_session()
    groups = session.query(CrazyKfcGroup).all()
    session.close()
    return groups
