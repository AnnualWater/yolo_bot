# -*- coding: utf-8 -*-
# @Author:归年丶似水
# @Email:2448955276@qq.com
# @GitHub:github.com/AnnualWater

from nonebot import get_driver, require, logger, get_bots
from nonebot.adapters.onebot.v11 import Message, Event, MessageSegment, MessageEvent, Bot, GroupMessageEvent, \
    ActionFailed
from nonebot.internal.matcher import Matcher
from nonebot.internal.params import Arg, ArgPlainText
from nonebot.plugin.on import on_startswith, on_fullmatch
from nonebot_plugin_apscheduler import scheduler

from .config import scheduled_job_minute
from .db_tools import add_comic_subscription, del_comic_subscription, search_comic_subscription, get_check_list, \
    update_comic_subscription
from .image_tools import get_search_list_image, get_scheduled_list_image
from .search_tools import search_comic, search_comic_by_id

require("nonebot_plugin_apscheduler")
require('db_sqlalchemy')

global_config = get_driver().config


async def send_update_message(title, now_episode, platform, create_user_id, group_id, bots, last_url: str):
    """
    尝试发布更新信息
    :param title: 番剧名
    :param now_episode:当前信息
    :param platform: 平台
    :param create_user_id:用户ID
    :param group_id: 群号
    :param bots: 机器人列表
    :param last_url: 最后一集的URL
    :return:是否已发送
    """
    msg = f"番剧[{title}]->[{platform}]更新了！{now_episode}\n" \
          f"{last_url}"
    send = False
    for bot_id in bots:
        bot: Bot = bots[bot_id]
        try:
            if group_id == 0:
                await bot.send_private_msg(user_id=create_user_id, message=msg)
            else:
                await bot.send_group_msg(group_id=group_id, message=msg)
        except ActionFailed:
            # 发送失败则有可能机器人不在此群
            continue
        # 发送成功则直接结束，防止重复发送
        send = True
        break
    return send


# 定时任务，查询番剧更新信息并发布
@scheduler.scheduled_job("interval", minutes=scheduled_job_minute)
async def comic_scheduled_check():
    logger.info("检查番剧更新")
    # 检查已经连接的机器人
    bots = get_bots()
    if len(bots) == 0:
        return
    # 获取数据库内容
    data = get_check_list()
    # 遍历番剧ID
    for (comic_id, platform) in data:
        # 获取番剧信息
        info = search_comic_by_id(comic_id, platform=platform)
        # 校验番剧是否与数据库内更新信息相同
        for item in data[(comic_id, platform)]:
            if info["now_episode"] == item["episode"]:
                # 相同则跳过
                continue
            # 不同则发布更新
            send = await send_update_message(title=info["title"], now_episode=info["now_episode"], platform=platform,
                                             create_user_id=item["create_user_id"], group_id=item["group_id"],
                                             bots=bots, last_url=info["last_url"])
            # 更改数据库信息
            if send:
                update_comic_subscription(create_user_id=item["create_user_id"], group_id=item["group_id"],
                                          comic_id=comic_id, platform=platform, episode=info["now_episode"])


# 番剧搜索
comic_search = on_startswith(msg="番剧搜索")


# 参数设定
@comic_search.handle()
async def handle_first(matcher: Matcher, event: MessageEvent):
    args = event.raw_message.split(" ")
    if len(args) > 1:
        matcher.set_arg("search", Message(args[1]))


# 获取参数
@comic_search.got("search", prompt="请输入搜索关键字")
# 执行搜索
async def handle_search(e: Event, search: Message = Arg(), search_str=ArgPlainText("search")):
    await comic_search.send("正在搜索，请稍后...")
    res = search_comic(search_str)
    if len(res) == 0:
        await comic_search.finish("未查找到任何番剧")
    img = await get_search_list_image(e.get_user_id(), res)
    # 发送搜索列表的图片
    await comic_search.send(MessageSegment.image(f"base64://{img}"))


class Parameter:
    """
    指令解析类
    """

    def __init__(self, event: MessageEvent, requre_comic_id=True):
        """
        生成对象并直接进行指令解析
        :param event:
        :param requre_comic_id:
        """
        self.user_id = event.user_id
        self.group_id = event.group_id if isinstance(event, GroupMessageEvent) else None
        plain_text = event.raw_message
        args = plain_text.split(" ")
        # 解析指令
        self.platform = "樱花"
        # 私聊解析-g
        if self.group_id is None:
            try:
                i = args.index("-g")
                try:
                    g = int(args[i + 1])
                    self.group_id = g
                except ValueError:
                    self.err = "参数-g解析失败"
                    return
            except ValueError:
                pass
        try:
            i = args.index("-p")
            print(i)
            self.platform = args[i + 1]
        except ValueError:
            pass
        if requre_comic_id:
            try:
                self.comic_id = int(args[1])
            except (ValueError, IndexError):
                self.err = "番剧ID解析失败"
                return
        self.scheduled_type = "private"
        self.err = None
        return

    async def check_role(self, bot: Bot, event: MessageEvent):
        # 是群订阅需要权限认证
        if self.group_id is not None:
            is_super_user = str(event.user_id) in bot.config.superusers
            if not is_super_user:
                info = await bot.get_group_member_info(group_id=self.group_id, user_id=self.user_id)
                if info["role"] not in ["owner", "admin"]:
                    self.err = "权限不足"
                    return
            self.scheduled_type = "group"
        return


# 番剧订阅
comic_scheduled = on_startswith(msg="番剧订阅")


@comic_scheduled.handle()
async def handle_first(bot: Bot, event: MessageEvent):
    await comic_scheduled.send("正在获取番剧信息，请稍后...")
    argv = Parameter(event)
    if argv.err is not None:
        await comic_scheduled.finish(argv.err)
        return
    await argv.check_role(bot, event)
    if argv.err is not None:
        await comic_scheduled.finish(argv.err)
        return
    # 认证通过则进行添加
    msg = f"群[{argv.group_id}]\n"
    if argv.group_id is None:
        msg = f"私[{argv.user_id}]\n"
        argv.group_id = 0
    comic_info = search_comic_by_id(comic_id=str(argv.comic_id), platform=argv.platform)
    db_info = add_comic_subscription(create_user_id=argv.user_id, group_id=argv.group_id, comic_id=str(argv.comic_id),
                                     title=comic_info["title"], platform=argv.platform,
                                     episode=comic_info["now_episode"], update_info=comic_info['update_info'],
                                     scheduled_type=argv.scheduled_type)
    if db_info != "success":
        await comic_scheduled.finish(db_info)
        return
    msg += (f"订阅[{comic_info['title']}]->[{argv.platform}]成功！\n"
            f"当前：{comic_info['now_episode']}\n"
            f"更新信息：{comic_info['update_info']}")
    await comic_scheduled.send(msg)


# 取消订阅
comic_del = on_startswith(msg=("番剧删除", "番剧取消"))


@comic_del.handle()
async def handle_first(bot: Bot, event: MessageEvent):
    argv = Parameter(event)
    if argv.err is not None:
        await comic_del.finish(argv.err)
        return
    await argv.check_role(bot, event)
    if argv.err is not None:
        await comic_del.finish(argv.err)
        return
    # 认证通过进行删除
    db_info = del_comic_subscription(create_user_id=argv.user_id, group_id=argv.group_id, comic_id=str(argv.comic_id),
                                     platform=argv.platform)
    if db_info != "success":
        await comic_del.finish(db_info)
        return
    await comic_del.send("删除订阅成功")


# 查询订阅列表
comic_ls = on_fullmatch(msg=("番剧列表", "订阅列表"))


@comic_ls.handle()
async def handle_first(event: MessageEvent):
    argv = Parameter(event, requre_comic_id=False)
    if argv.err is not None:
        await comic_del.finish(argv.err)
        return
    if argv.group_id is not None:
        argv.scheduled_type = "group"
    # 进行查询
    objs = search_comic_subscription(create_user_id=argv.user_id, group_id=argv.group_id)
    if len(objs) == 0:
        await comic_ls.finish("没有订阅")
        return
    data = []
    # 循环进行表转置
    for item in objs:
        data.append(
            {"番剧ID": item.comic_id, "番剧名称": item.title, "当前": item.episode, "更新信息": item.update_info,
             "platform": item.platform})
    img = await get_scheduled_list_image(argv.user_id, data)
    # 发送订阅列表的图片
    await comic_search.send(MessageSegment.image(f"base64://{img}"))
