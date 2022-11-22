# -*- coding: utf-8 -*-
# @Author:归年丶似水
# @Email:2448955276@qq.com
# @GitHub:github.com/AnnualWater

import base64
import os
import re
from pathlib import Path

from dominate.tags import *
from pyppeteer import launch


def get_default_html(css_path: str):
    """
    生成默认的HTML
    :param css_path:需要导入的css的文件位置
    :return: dominate doc
    """
    doc = html(lang="en")
    with doc.add(head()):
        title("get_music_list_image")
        meta(content="text/html; charset=utf-8", http_equiv="Content-Type")
    # 获取css
    if css_path is not None:
        with open(css_path, encoding="utf-8") as css_file:
            css = css_file.read()
            # 将CSS进行简化
            css = re.sub(r'\s{4}|\t|\n', '', css)
            doc.add(style(css))
    return doc


def get_default_table(data: list[dict], table_head: dict[str:str]):
    """
    生成默认的HTML列表
    :param data: 列表
    :param table_head:表头
    :return: dominate table
    """
    data_table = table()
    # 添加表头
    table_tr = tr()
    for key in table_head:
        table_tr += td(table_head[key])
    data_table.add(thead(table_tr))
    # 添加内容
    for item in data:
        data_tr = tr()
        for key in table_head:
            data_tr += td(item[key])
        data_table.add(data_tr)
    return data_table


def save_html(file_path, doc):
    """
    保存html文件
    :param file_path:保存位置
    :param doc: dominate doc
    :return:None
    """
    Path(file_path).parent.mkdir(parents=True, exist_ok=True)
    with open(file_path, mode="a", encoding="utf-8") as file:
        # 首先清空文件
        file.truncate(0)
        # 重新写入
        file.write(doc.render(pretty=False))


async def screenshot(file_path, query: str):
    """
    截图
    :param file_path: HTML文件位置
    :param query: 截图元素的指定ID
    :return: 图片的base64
    """
    # 用pyppeteer打开
    browser = await launch(options={"headless": True})
    page = await browser.newPage()
    await page.goto(url=f"file:///{os.path.abspath(file_path)}")
    # 根据ID寻找指定元素截图
    container = await page.querySelector(query)
    image_byte = await container.screenshot()
    await browser.close()
    return base64.b64encode(image_byte).decode()
