# -*- coding: utf-8 -*-
# @Author:归年丶似水
# @Email:2448955276@qq.com
# @GitHub:github.com/AnnualWater

from argparse import Namespace

from nonebot.adapters.onebot.v11 import Bot, Event, MessageSegment
from nonebot.internal.matcher import Matcher

from .db_tools import add_custom_reply, get_custom_reply_list, table_transform, del_custom_reply, get_custom_reply_by_id
from .image_tools import get_custom_reply_list_image


class Handle:
    """
    处理指令的类
    鸭子模式的方法
    参数表皆为(cls, args: Namespace, bot: Bot, event: Event, matcher: Matcher)
    """

    @staticmethod
    async def reply(args: Namespace, bot: Bot, message):
        """
        回复消息
        :param args:指令参数
        :param bot: bot
        :param message:消息
        :return: None
        """
        if args.conv["group"] is None:
            await bot.send_private_msg(user_id=args.conv["user"], message=message)
        else:
            await bot.send_group_msg(group_id=args.conv["group"], message=message)

    @classmethod
    async def help(cls, args: Namespace, bot: Bot, event: Event, matcher: Matcher):
        """
        帮助指令
        :param args:
        :param bot:
        :param event:
        :param matcher:
        :return:
        """
        print(args)
        help_msg = ""
        if args.action == "None":
            help_msg = ('Custom Reply帮助信息\n'
                        '   help:帮助\n'
                        '   ls:查看列表\n'
                        '   add:添加\n'
                        '   del:删除\n'
                        '   键入指令>crm help -a [操作名]')
        elif args.action == "ls":
            help_msg = "ls_help"
        await cls.reply(args, bot, help_msg)

    @classmethod
    async def ls(cls, args: Namespace, bot: Bot, event: Event, matcher: Matcher):
        """
        查看列表指令
        :param args:
        :param bot:
        :param event:
        :param matcher:
        :return:
        """

        async def __do_work(group_id, create_user_id):
            __items = get_custom_reply_list(group_id=group_id, create_user_id=create_user_id)
            __items = table_transform(__items)
            img = await get_custom_reply_list_image(args.conv["user"], __items)
            await cls.reply(args, bot, MessageSegment.image(f"base64://{img}"))

        # 如果是私聊消息
        if args.conv["group"] is None:
            # 如果参数群号不为None
            if args.group is not None:
                # 如果不是是超级用户
                if not args.is_super_user:
                    # 获取成员在群内的信息
                    info = await bot.get_group_member_info(group_id=args.group, user_id=args.conv["user"])
                    if info["role"] not in ["owner", "admin"]:
                        await cls.reply(args, bot, "权限不足")
                        return
                # 执行获取群的自定义消息列表
                await __do_work(group_id=args.group, create_user_id=None)
                return
            else:
                # 执行获取私聊的自定义消息列表
                await __do_work(group_id=None, create_user_id=args.user)
                return
        else:
            # 群消息直接执行获取群的自定义消息列表
            await __do_work(group_id=args.conv["group"], create_user_id=None)
            return

    @classmethod
    async def add(cls, args: Namespace, bot: Bot, event: Event, matcher: Matcher):
        """
        添加指令
        :param args:
        :param bot:
        :param event:
        :param matcher:
        :return:
        """

        # 获取参数
        args.message = matcher.get_arg(key="message")

        # 如果是私聊消息
        if args.conv["group"] is None:
            # 如果参数群号不为None
            if args.group is not None:
                # 如果不是是超级用户
                if not args.is_super_user:
                    # 获取成员在群内的信息
                    info = await bot.get_group_member_info(group_id=args.group, user_id=args.conv["user"])
                    if info["role"] not in ["owner", "admin"]:
                        await cls.reply(args, bot, "权限不足")
                        return
                    # 执行添加方法
                    add_custom_reply(message=str(args.message),
                                     is_regex=args.regex,
                                     command=args.command,
                                     group_id=args.group,
                                     response_type=args.type,
                                     create_user_id=args.user)
                    await cls.reply(args, bot, "添加成功")
                    return
            else:
                # 私聊自定义
                add_custom_reply(message=str(args.message),
                                 is_regex=args.regex,
                                 command=args.command,
                                 group_id=0,
                                 response_type="private",
                                 create_user_id=args.user)
                await cls.reply(args, bot, "添加成功")
                return
        else:
            # 群消息无视传入的群号
            args.group = args.conv["group"]
            # 如果是群内私聊自定义则直接执行
            if args.type == "group_private":
                # 直接执行
                add_custom_reply(message=str(args.message),
                                 is_regex=args.regex,
                                 command=args.command,
                                 group_id=args.group,
                                 response_type="group_private",
                                 create_user_id=args.user)
                return
                # 获取成员在群内的权限
            if not args.is_super_user:
                # 获取成员在群内的信息
                info = await bot.get_group_member_info(group_id=args.group, user_id=args.conv["user"])
                if info["role"] not in ["owner", "admin"]:
                    await cls.reply(args, bot, "权限不足")
                    return
                # 直接执行
                add_custom_reply(message=str(args.message),
                                 is_regex=args.regex,
                                 command=args.command,
                                 group_id=args.group,
                                 response_type="group_private",
                                 create_user_id=args.user)
                return

    @classmethod
    async def rm(cls, args: Namespace, bot: Bot, event: Event, matcher: Matcher):
        # 超级管理直接删除
        if args.is_super_user:
            del_custom_reply(args.id)
            await cls.reply(args=args, bot=bot, message="删除成功")
            return
            # 获取要删除的自定义回复
        obj = get_custom_reply_by_id(args.id)
        # 如果是私聊
        if obj.group_id == 0:
            # 比对用户ID
            if obj.create_user_id == args.conv["user"]:
                del_custom_reply(args.id)
                await cls.reply(args=args, bot=bot, message="删除成功")
                return
            else:
                await cls.reply(args=args, bot=bot, message="权限不足，请检查ID是否有误")
                return
        else:
            # 群消息需要获取成员在群内的信息
            info = await bot.get_group_member_info(group_id=args.group, user_id=args.conv["user"])
            if info["role"] not in ["owner", "admin"]:
                await cls.reply(args, bot, "权限不足")
                return
            del_custom_reply(args.id)
            await cls.reply(args=args, bot=bot, message="删除成功")
            return
