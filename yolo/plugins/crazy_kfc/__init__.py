# -*- coding: utf-8 -*-
# @Author:归年丶似水
# @Email:2448955276@qq.com
# @GitHub:github.com/AnnualWater

import json
import random
from datetime import datetime

from nonebot import on_regex, require, logger, get_bots
from nonebot.adapters.onebot.v11 import Bot, MessageEvent, GroupMessageEvent
from nonebot.exception import ActionFailed
from nonebot_plugin_apscheduler import scheduler

from .db_tools import add_group, del_group

require("nonebot_plugin_apscheduler")
require("db_sqlalchemy")


@scheduler.scheduled_job("interval", weeks=1, start_date=datetime(2022, 1, 6, 10, 30, 0))
async def crazy_scheduled():
    logger.info("疯狂星期四")
    # 检查已经连接的机器人
    bots = get_bots()
    if len(bots) == 0:
        return
    groups = []
    for group_id in groups:
        for bot_id in bots:
            bot: Bot = bots[bot_id]
            try:
                await bot.send_group_msg(group_id=group_id, message=get_crazy())
            except ActionFailed:
                # 发送失败则有可能机器人不在此群
                continue
            # 发送成功则直接结束，防止重复发送
            break


def get_crazy():
    with open("./yolo/data/crazy_kfc.json", "r", encoding="utf-8") as f:
        kfc = json.load(f).get("post")
        msg = random.choice(kfc)
        return msg


crazy = on_regex(pattern=r"疯狂星期四")


@crazy.handle()
async def _(event: MessageEvent):
    group = event.group_id if isinstance(event, GroupMessageEvent) else None
    if group is not None:
        add_group(group)
    await crazy.send(get_crazy())


crazy_del = on_regex(pattern=r"平静星期四")


@crazy_del.handle()
async def _(event: GroupMessageEvent):
    del_group(event.group_id)
    await crazy_del.send("疯狂的星期四已归为平静")
