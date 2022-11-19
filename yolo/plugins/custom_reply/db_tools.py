# -*- coding: utf-8 -*-
# @Author:归年丶似水
# @Email:2448955276@qq.com
# @GitHub:github.com/AnnualWater

from yolo.plugins.db_sqlalchemy import get_session

from .domain import CustomReplyDbItem

cache: dict[str:dict] | None = None


def reset_cache():
    global cache

    cache = {"group": {},
             "private": {}}
    session = get_session()
    objs = session.query(CustomReplyDbItem).all()
    session.close()
    for obj in objs:
        if obj.group_id == 0:
            if obj.create_user_id not in cache["private"].keys():
                cache["private"][obj.create_user_id] = []
            cache["private"][obj.create_user_id].append(obj)
        else:
            if obj.group_id not in cache["group"].keys():
                cache["group"][obj.group_id] = []
            cache["group"][obj.group_id].append(obj)


def get_reply_full_list() -> dict[str, dict[int, list[CustomReplyDbItem]]]:
    if cache is None:
        reset_cache()
    return cache


def table_transform(objs: list[CustomReplyDbItem]):
    """
    表转置函数
    :param objs: 数据库查询的obj
    :return:
    """
    rep = []
    for item in objs:
        rep.append({
            "id": item.id,
            "create_user_id": item.create_user_id,
            "group_id": item.group_id,
            "message": item.message,
            "command": item.command,
            "is_regex": item.is_regex,
            "response_type": item.response_type
        })
    return rep


def add_custom_reply(
        message: str,
        is_regex: bool,
        command: str,
        group_id: int,
        response_type: str,
        create_user_id: int):
    """
    添加自定义回复
    :param message: 回复消息
    :param is_regex:是否使用正则
    :param command:检测命令
    :param group_id:群号
    :param response_type:指令检测类型 private group group_private
    :param create_user_id:用户ID
    :return:
    """
    session = get_session()
    cr = CustomReplyDbItem(
        message=message,
        is_regex=is_regex,
        command=command,
        group_id=group_id,
        response_type=response_type,
        create_user_id=create_user_id)
    session.add(cr)
    session.commit()
    session.close()
    reset_cache()


def get_custom_reply_list(
        group_id: int | None,
        create_user_id: int | None):
    """
    获取自定义回复的列表
    :param group_id:群号
    :param create_user_id:用户ID
    :return:
    """
    session = get_session()
    query = session.query(CustomReplyDbItem)
    if group_id is not None:
        query = query.filter(CustomReplyDbItem.group_id == group_id)
    else:
        query = query.filter(CustomReplyDbItem.group_id == 0)
    if create_user_id is not None:
        query = query.filter(CustomReplyDbItem.create_user_id == create_user_id)
    objs = query.all()
    session.close()
    return objs


def del_custom_reply(__id: int):
    """
    根据ID删除自定义回复
    :param __id: ID
    :return:
    """
    session = get_session()
    obj = session.query(CustomReplyDbItem).get(__id)
    session.delete(obj)
    session.commit()
    session.close()
    pass


def get_custom_reply_by_id(__id: int) -> CustomReplyDbItem | None:
    """
    根据ID获取自定义回复
    :param __id: ID
    :return: obj
    """
    session = get_session()
    obj = session.query(CustomReplyDbItem).get(__id)
    session.close()
    return obj
