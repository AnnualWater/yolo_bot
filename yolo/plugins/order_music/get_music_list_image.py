# -*- coding: utf-8 -*-
# @Author:归年丶似水
# @Email:2448955276@qq.com
# @GitHub:github.com/AnnualWater

import os.path

from dominate.tags import *
from nonebot import get_driver

from yolo.tools.html import get_default_html, get_default_table, save_html, screenshot

global_config = get_driver().config


async def get_music_list_image(user_id: str, music_list: list[dict[str, str] | dict[str, str]]) -> str:
    file_path = os.path.abspath(f"{global_config.html_data}/{user_id}/order_music.html")
    # 生成html
    doc = get_default_html(f"{global_config.css_path}/default_table.css")
    container = div(cls="frame", id="container")
    container += div("搜索结果如下,请输入歌曲序号", cls="search")
    # 生成列表
    music_table = get_default_table(music_list, {
        "id": "序号",
        "song_name": "歌曲名",
        "artist_name": "歌手",
        "platform": "来源"
    })
    container.add(music_table)
    doc.add(body(container))
    # 保存html
    save_html(file_path, doc)
    return await screenshot(file_path, "#container")
