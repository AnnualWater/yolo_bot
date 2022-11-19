# -*- coding: utf-8 -*-
# @Author:归年丶似水
# @Email:2448955276@qq.com
# @GitHub:github.com/AnnualWater
import os

from dominate.tags import *
from nonebot import get_driver

from yolo.tools.html import get_default_html, get_default_table, save_html, screenshot

global_config = get_driver().config


async def get_custom_reply_list_image(user_id, res):
    """
    获取当前订阅列表的图片
    :param user_id: 用户ID，用于文件名
    :param res: 数据列表
    :return: 图片的base64
    """
    file_path = os.path.abspath(f"{global_config.html_data}/{user_id}/custom_reply_list.html")
    doc = get_default_html(f"{global_config.css_path}/default_table.css")
    container = div(cls="frame", id="container")
    container += div("群自定义回复列表", cls="search")
    comic_table = get_default_table(res, {
        "id": "ID",
        "create_user_id": "用户ID",
        "group_id": "群号",
        "message": "自定义消息",
        "command": "指令",
        "is_regex": "启用正则",
        "response_type": "回复类型"
    })
    container.add(comic_table)
    doc.add(body(container))
    # 保存html
    save_html(file_path, doc)
    return await screenshot(file_path, "#container")
