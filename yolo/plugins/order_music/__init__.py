# -*- coding: utf-8 -*-
# @Author:归年丶似水
# @Email:2448955276@qq.com
# @GitHub:github.com/AnnualWater

import re

from nonebot import get_driver
from nonebot.adapters.onebot.v11 import MessageSegment, Message, Event
from nonebot.matcher import Matcher
from nonebot.params import CommandArg, Arg, ArgPlainText
from nonebot.plugin.on import on_command

from .config import max_search
from .get_music_list_image import get_music_list_image
from .search_music import search_music

global_config = get_driver().config

order = on_command("点歌")
music_list: dict[str, list[dict[str, str] | dict[str, str]]] = {}


@order.handle()
async def handle_first(matcher: Matcher, args: Message = CommandArg()):
    plain_text = args.extract_plain_text()
    if plain_text:
        matcher.set_arg("search", args)


@order.got("search", prompt="请输入关键词")
async def handle_search(e: Event, search: Message = Arg(), search_str=ArgPlainText("search")):
    user_id = e.get_user_id()
    music_list[user_id] = []
    # 从163和qq搜索
    result_163 = search_music(search_str, "163")
    result_tencent = search_music(search_str, "qq")
    if len(result_163) == 0 and len(result_tencent) == 0:
        await order.finish(f"未搜索到{search_str}")
        return
    # 将搜索内容存入
    num = 1
    for obj in result_163:
        obj["id"] = num
        music_list[user_id].append(obj)
        num += 1
    for obj in result_tencent:
        obj["id"] = num
        music_list[user_id].append(obj)
        num += 1
    image = await get_music_list_image(user_id, music_list[user_id])
    # 发送搜索列表的图片
    await order.send(MessageSegment.image(f"base64://{image}"))


@order.got("music_id")
async def handle_send_music(e: Event, music_id: Message = Arg(), music_id_str=ArgPlainText("music_id")):
    id_m = re.match('^[0-9]+$', music_id_str)
    if id_m is None:
        await order.reject("输入的歌曲ID有误，请重新输入")
    user_id = e.get_user_id()
    num = int(id_m.group())
    music = list(filter(lambda x: x["id"] == num, music_list[user_id]))
    if len(music) == 0:
        await order.reject("输入的歌曲ID超出范围，请重新输入")
    music = music[0]
    await order.send(MessageSegment.music(music["platform"], int(music["song_id"])))
