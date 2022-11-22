# -*- coding: utf-8 -*-
# @Author:归年丶似水
# @Email:2448955276@qq.com
# @GitHub:github.com/AnnualWater

from sqlalchemy import select

from yolo.plugins.db_sqlalchemy import get_session
from .domain import ComicSubscriptionInfo


def __find_first(session, group_id, create_user_id, comic_id, platform):
    """
    查找数据库内第一个符合条件的数据
    :param session:数据库session
    :param group_id:群号
    :param create_user_id:用户ID
    :param comic_id:番剧ID
    :param platform:番剧平台
    :return:
    """
    # 查重
    query = (session.query(ComicSubscriptionInfo)
             .filter(ComicSubscriptionInfo.comic_id == comic_id)
             .filter(ComicSubscriptionInfo.platform == platform))
    if group_id == 0:
        query = query.filter(ComicSubscriptionInfo.create_user_id == create_user_id) \
            .filter(ComicSubscriptionInfo.scheduled_type == "private")
    else:
        query = query.filter(ComicSubscriptionInfo.group_id == group_id) \
            .filter(ComicSubscriptionInfo.scheduled_type == "group")
    return query.first()


def add_comic_subscription(
        create_user_id: int,
        group_id: int,
        comic_id: str,
        title: str,
        platform: str,
        episode: str,
        update_info: str,
        scheduled_type: str
):
    """
    添加番剧订阅
    :param create_user_id: 用户ID
    :param group_id: 群号
    :param comic_id: 番剧ID
    :param title: 番剧标题
    :param platform: 番剧平台
    :param episode: 番剧当前信息
    :param update_info: 番剧更新信息
    :param scheduled_type: 番剧订阅类型 private group
    :return:ErrMsg | "success"
    """
    session = get_session()
    # 查重
    obj = __find_first(session, group_id, create_user_id, comic_id, platform)
    if obj is not None:
        session.close()
        return "订阅重复"
    # 添加
    cr = ComicSubscriptionInfo(
        create_user_id=create_user_id,
        group_id=group_id,
        comic_id=comic_id,
        title=title,
        platform=platform,
        episode=episode,
        update_info=update_info,
        scheduled_type=scheduled_type
    )
    session.add(cr)
    session.commit()
    session.close()
    if cache_check_list is None:
        __reset_cache_check_list()
    else:
        if (comic_id, platform) not in cache_check_list:
            cache_check_list[(comic_id, platform)] = []
        cache_check_list[(comic_id, platform)].append(
            {"create_user_id": create_user_id, "group_id": group_id, "episode": episode})
    return "success"


def del_comic_subscription(create_user_id: int, group_id: int, comic_id: str, platform: str):
    """
    删除订阅
    :param create_user_id: 用户ID
    :param group_id: 群号
    :param comic_id: 番剧ID
    :param platform: 番剧平台
    :return:ErrMsg | "success"
    """
    session = get_session()
    obj = __find_first(session, group_id, create_user_id, comic_id, platform)
    if obj is None:
        session.close()
        return "订阅不存在"
    # 执行删除
    session.delete(obj)
    session.commit()
    session.close()
    __reset_cache_check_list()
    return "success"


def update_comic_subscription(create_user_id: int, group_id: int, comic_id: str, platform: str, episode: str):
    """
    更新番剧当前信息
    :param create_user_id: 用户ID
    :param group_id: 群号
    :param comic_id: 番剧ID
    :param platform: 番剧平台
    :param episode: 新的当前信息
    :return: ErrMsg | "success"
    """
    session = get_session()
    obj = __find_first(session, group_id, create_user_id, comic_id, platform)
    if obj is None:
        session.close()
        return "订阅不存在"
    # 执行更改
    print(obj)
    obj.episode = episode
    session.commit()
    session.close()
    __reset_cache_check_list()
    return "success"


def search_comic_subscription(create_user_id, group_id):
    """
    查找番剧订阅
    :param create_user_id: 用户ID
    :param group_id: 群号
    :return:所有符合条件的ComicSubscriptionInfo
    """
    session = get_session()
    query = session.query(ComicSubscriptionInfo)
    if group_id == 0:
        query = query.filter(ComicSubscriptionInfo.create_user_id == create_user_id) \
            .filter(ComicSubscriptionInfo.scheduled_type == "private")
    else:
        query = query.filter(ComicSubscriptionInfo.group_id == group_id) \
            .filter(ComicSubscriptionInfo.scheduled_type == "group")
    objs = query.all()
    session.close()
    return objs


# 番剧订阅缓存
cache_check_list: dict | None = None


def __reset_cache_check_list():
    """
    刷新番剧订阅缓存
    :return: None
    """
    global cache_check_list
    session = get_session()
    query = select(ComicSubscriptionInfo.comic_id,
                   ComicSubscriptionInfo.platform,
                   ComicSubscriptionInfo.create_user_id,
                   ComicSubscriptionInfo.group_id,
                   ComicSubscriptionInfo.episode)
    objs = session.execute(query).all()
    rep = {}
    for obj in objs:
        if (obj[0], obj[1]) not in rep:
            rep[(obj[0], obj[1])] = []
        rep[(obj[0], obj[1])].append({"create_user_id": obj[2], "group_id": obj[3], "episode": obj[4]})
    session.close()
    cache_check_list = rep


def get_check_list():
    """
    获取番剧订阅列表
    用于定时任务
    :return:番剧订阅列表[key:番剧ID][value:list[dict]]
    """
    # 查询缓存
    if cache_check_list is None:
        __reset_cache_check_list()
    return cache_check_list.copy()
