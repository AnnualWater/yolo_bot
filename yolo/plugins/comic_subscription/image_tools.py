# -*- coding: utf-8 -*-
# @Author:归年丶似水
# @Email:2448955276@qq.com
# @GitHub:github.com/AnnualWater

import os

from dominate.tags import *
from nonebot import get_driver

from yolo.tools.html import get_default_html, get_default_table, save_html, screenshot

global_config = get_driver().config


async def get_search_list_image(user_id, res):
    """
    获取关键字搜索番剧的列表图片
    :param user_id: 用户ID，用于文件名
    :param res: 数据列表
    :return: 图片的base64
    """
    file_path = os.path.abspath(f"{global_config.html_data}/{user_id}/comic_search.html")
    doc = get_default_html(f"{global_config.css_path}/default_table.css")
    container = div(cls="frame", id="container")
    container += div("搜索结果如下，输入 番剧订阅[番剧ID] 订阅", cls="search")
    comic_table = get_default_table(res, {
        "番剧ID": "番剧ID",
        "番剧名称": "番剧名称",
        "更新信息": "更新信息",
        "platform": "番剧来源"
    })
    container.add(comic_table)
    doc.add(body(container))
    # 保存html
    save_html(file_path, doc)

    return await screenshot(file_path, "#container")


async def get_scheduled_list_image(user_id, res):
    """
    获取当前订阅列表的图片
    :param user_id: 用户ID，用于文件名
    :param res: 数据列表
    :return: 图片的base64
    """
    file_path = os.path.abspath(f"{global_config.html_data}/{user_id}/scheduled_list.html")
    doc = get_default_html(f"{global_config.css_path}/default_table.css")
    container = div(cls="frame", id="container")
    container += div("群订阅列表，输入 番剧删除[番剧ID] 删除订阅", cls="search")
    comic_table = get_default_table(res, {
        "番剧ID": "番剧ID",
        "番剧名称": "番剧名称",
        "当前": "当前更新",
        "更新信息": "更新信息",
        "platform": "番剧来源"
    })
    container.add(comic_table)
    doc.add(body(container))
    # 保存html
    save_html(file_path, doc)
    return await screenshot(file_path, "#container")
