# -*- coding: utf-8 -*-
# @Author:归年丶似水
# @Email:2448955276@qq.com
# @GitHub:github.com/AnnualWater

from .domain import UserSignInfo
from ..db_sqlalchemy import get_session


def try_use(money: int, user_id: int) -> bool:
    session = get_session()
    info = session.query(UserSignInfo).get(user_id)
    if info.money < money:
        session.close()
        return False
    else:
        info.money -= money
    session.commit()
    session.close()
    return True
