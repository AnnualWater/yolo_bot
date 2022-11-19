# -*- coding: utf-8 -*-
# @Author:归年丶似水
# @Email:2448955276@qq.com
# @GitHub:github.com/AnnualWater

import json

import requests
from nonebot import get_driver

from .config import max_search

global_config = get_driver().config


# noinspection HttpUrlsUsage
def search_music(search: str, platform: str):
    search_url = ""
    headers = {}
    # 根据不同平台设定不同的搜索地址
    if platform == "163":
        search_url = f"http://music.163.com/api/search/get/web?s={search}&type=1&offset=0&total=true"
        headers = {
            'Referer': 'http://music.163.com'
        }

    elif platform == "qq":
        search_url = f"http://c.y.qq.com/soso/fcgi-bin/search_for_qq_cp?format=json&p=0&n=5&w={search}"
        headers = {
            'Referer': 'http://c.y.qq.com'
        }
    response = requests.request("GET", url=search_url, headers=headers)
    rep_list = []

    if response.status_code == 200:
        i = 0
        data = json.loads(response.text)
        # 解析指令
        if platform == "163":
            if data["code"] != 200:
                return rep_list
            for song in data["result"]["songs"]:
                singers = ""
                for a in song["artists"]:
                    singers += a["name"] + "、"
                rep_list.append({"song_name": song["name"],
                                 "artist_name": singers[:-1],
                                 "song_id": song["id"],
                                 "platform": platform})
                if i >= max_search:
                    return rep_list
                i += 1
        elif platform == "qq":
            for song in data["data"]["song"]["list"]:
                singers = ""
                for a in song["singer"]:
                    singers += a["name"] + "、"
                rep_list.append({"song_name": song["songname"],
                                 "artist_name": singers[:-1],
                                 "song_id": song["songid"],
                                 "platform": platform})
                if i >= max_search:
                    return rep_list
                i += 1
    # 未搜索到则返回空列表
    return rep_list
