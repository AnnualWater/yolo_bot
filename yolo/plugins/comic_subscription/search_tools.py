# -*- coding: utf-8 -*-
# @Author:归年丶似水
# @Email:2448955276@qq.com
# @GitHub:github.com/AnnualWater

import requests
from lxml import etree

from .config import search_comic_config, search_comic_by_id_config, headers


def search_comic(search: str) -> list[dict[str:str]]:
    """
    根据关键字查询番剧
    :param search:  搜索关键字
    :return: 搜索信息（根据config配置）
    """
    __config = search_comic_config
    # 返回一个字典
    response: list[dict[str:str]] = []
    for config_key in __config:
        # 列表的XPath
        x_path = __config[config_key]["x_path"]
        # 替换搜索关键字
        search_url = str(__config[config_key]["url"]).replace("{{search}}", search)
        # 发送请求
        res = requests.request(url=search_url, headers=headers, method="GET", timeout=15)
        html = etree.HTML(res.text)
        # 获取列表
        search_list = html.xpath(x_path)
        for search_item in search_list:
            item = {}
            for key in __config[config_key]["data"]:
                value = __config[config_key]["data"][key](search_item)
                item[key] = value
            response.append(item)
    return response


def search_comic_by_id(comic_id: str, platform: str):
    """
    根据番剧ID查询番剧信息
    :param comic_id: 番剧ID
    :param platform: 番剧平台
    :return: 搜索信息（根据config配置）
    """
    __config = search_comic_by_id_config[platform]
    response = {}
    search_url = str(__config["url"]).replace("{{comic_id}}", comic_id)
    # 发送请求
    res = requests.request(url=search_url, headers=headers, method="GET", timeout=15)
    html = etree.HTML(res.text)
    for key in __config["data"]:
        value = __config["data"][key](html)
        response[key] = value
    return response
