# -*- coding: utf-8 -*-
# @Author:归年丶似水
# @Email:2448955276@qq.com
# @GitHub:github.com/AnnualWater
import datetime

from nonebot import require, on_fullmatch
from nonebot.adapters.onebot.v11 import MessageEvent
from nonebot.internal.matcher import Matcher

from .domain import UserSignInfo
from .tools import *

require('db_sqlalchemy')

yolo_money = on_fullmatch(msg=("签到", "剩余yo币"))


async def sign(event: MessageEvent, matcher: Matcher):
    user_id = event.user_id
    # 从数据库获取信息
    session = get_session()
    info = session.query(UserSignInfo).get(user_id)

    if info is None:
        info = UserSignInfo(
            user_id=user_id,
            money=1600,
            last_sign=datetime.datetime.now(),
            continuous_sign=1
        )
        session.add(info)
        await matcher.send("首次签到成功！获得1600[yo币]")
    else:
        # 判断今天是否签到过了
        if is_today(info.last_sign):
            await matcher.send(f"今天已经在[{info.last_sign.strftime('%H:%M:%S')}]签到过了哦！")
            session.close()
            return
        info.continuous_sign += 1
        add_money = 60 + int(info.continuous_sign / 10) * 20
        info.money += add_money
        info.last_sign = datetime.datetime.now()
        await matcher.send(f"签到成功！连续签到{info.continuous_sign}天，获得{add_money}[yo币]\n"
                           f"剩余[yo币]：{info.money}")
    session.commit()
    session.close()


async def last_money(event: MessageEvent, matcher: Matcher):
    user_id = event.user_id
    # 从数据库获取信息
    session = get_session()
    info = session.query(UserSignInfo).get(user_id)
    session.close()
    if info is None:
        await matcher.send("从来都没有签到过哦！请先签到")
    else:
        await yolo_money.send(f"当前剩余[yo币]：{info.money}")


action = {
    "签到": sign,
    "剩余yo币": last_money
}


@yolo_money.handle()
async def _(event: MessageEvent, matcher: Matcher):
    await action[event.raw_message](event, matcher)


def is_today(target_date: datetime):
    """
    判断日期是否是今天
    """
    c_year = datetime.datetime.now().year
    c_month = datetime.datetime.now().month
    c_day = datetime.datetime.now().day

    t_year = target_date.year
    t_month = target_date.month
    t_day = target_date.day

    final = False
    if c_year == t_year and c_month == t_month and c_day == t_day:
        final = True
    return final
