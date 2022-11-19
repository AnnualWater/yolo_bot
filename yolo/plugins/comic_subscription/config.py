# -*- coding: utf-8 -*-
# @Author:归年丶似水
# @Email:2448955276@qq.com
# @GitHub:github.com/AnnualWater

import re

scheduled_job_minute = 12

headers = {'referer': 'https://www.google.com',
           'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                         'Chrome/72.0.3626.81 Safari/537.36 SE 2.X MetaSr 1.0'}


def get_comic_id(element):
    s = element.xpath("./h2/a/@href")
    return re.search(r"[0-9]+", s[0]).group()


def get_title(element):
    s = element.xpath("./h2/a/@title")
    return s[0]


def get_update_info(element):
    s = element.xpath("./span[1]/font/text()")
    if len(s) > 0:
        return s[0]
    return ""


# 关键词搜索番剧的配置
search_comic_config = {
    "樱花": {
        "url": "https://www.yhdmp.net/s_all?ex=1&kw={{search}}",
        "urls": ["https://www.yhdmp.net/s_all?ex=1&kw={{search}}",
                 "https://www.yhdmp.live/s_all?ex=1&kw={{search}}",
                 "https://www.yhdmp.cc/s_all?ex=1&kw={{search}}",
                 "https://www.yhdmp.com/s_all?ex=1&kw={{search}}", ],
        "x_path": "//div[@class='lpic']/ul/li",
        "data": {
            "番剧ID": get_comic_id,
            "番剧名称": get_title,
            "更新信息": get_update_info,
            "platform": lambda x: "樱花"
        }
    }
}


def get_title(element):
    s = element.xpath("//div[@class='rate r']/h1/text()")
    return s[0]


def get_now_episode(element):
    s = element.xpath("//div[@class='sinfo']/p[2]/text()")
    return s[0]


def get_update_info(element):
    s = element.xpath("//div[@class='sinfo']/p[2]/font/text()")
    return s[0]


def get_last_url(element):
    s = element.xpath("//div[@class='tabs']/div/div[2]/ul/li[last()]/a/@href")
    return f"https://www.yhdmp.live{s[0]}"


# 根据ID获取番剧信息的配置
search_comic_by_id_config = {
    "樱花": {
        "url": "https://www.yhdmp.net/showp/{{comic_id}}.html",
        "urls": ["https://www.yhdmp.net/showp/{{comic_id}}.html",
                 "https://www.yhdmp.live/showp/{{comic_id}}.html",
                 "https://www.yhdmp.cc/showp/{{comic_id}}.html"
                 "https://www.yhdmp.com/showp/{{comic_id}}.html"],
        "data": {
            "title": get_title,
            "now_episode": get_now_episode,
            "update_info": get_update_info,
            "last_url": get_last_url
        }
    }
}
