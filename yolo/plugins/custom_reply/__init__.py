# -*- coding: utf-8 -*-
# @Author:归年丶似水
# @Email:2448955276@qq.com
# @GitHub:github.com/AnnualWater
import re
from argparse import Namespace

from nonebot import require
from nonebot.adapters.onebot.v11 import MessageEvent, Bot, GroupMessageEvent, Message
from nonebot.exception import ParserExit
from nonebot.internal.matcher import Matcher
from nonebot.internal.params import Arg
from nonebot.params import ShellCommandArgs
from nonebot.plugin.on import on_shell_command, on_message

from .db_tools import get_reply_full_list
from .domain import CustomReplyDbItem
from .handle import Handle
from .parser import crm_parser

require('db_sqlalchemy')

custom_reply = on_message()


@custom_reply.handle()
async def _(event: MessageEvent):
    async def __do_check(__items: list):
        for __item in __items:
            # 判定是否符合条件
            if __item.is_regex:
                # 正则
                r = re.search(__item.command, raw_text)
                if r is not None:
                    # 回复
                    await custom_reply.send(Message(__item.message))
            else:
                if __item.command == raw_text:
                    await custom_reply.send(Message(__item.message))

    # 获取缓存
    replies = get_reply_full_list()
    raw_text = event.message.extract_plain_text()
    user = event.user_id
    group = event.group_id if isinstance(event, GroupMessageEvent) else None
    if group is not None:
        # 如果是群聊
        if group not in replies["group"]:
            return
        items = replies["group"][group]
        await __do_check(items)
    else:
        # 如果是私聊
        if user not in replies["private"]:
            return
        items = replies["private"][user]
        await __do_check(items)


custom_reply_command = on_shell_command("crm", parser=crm_parser)


async def __func(bot: Bot, event: MessageEvent, args: Namespace):
    args.conv = {
        "user": event.user_id,
        "group": event.group_id if isinstance(event, GroupMessageEvent) else None
    }
    # 是否是超级用户
    args.is_super_user = str(event.user_id) in bot.config.superusers
    # 覆盖user参数
    args.user = args.conv["user"]
    if args.handle is not None:
        return args.handle, getattr(Handle, args.handle)
    else:
        await custom_reply_command.reject("请输入操作！")
    await custom_reply_command.finish()
    return None


@custom_reply_command.handle()
async def _(foo: ParserExit = ShellCommandArgs()):
    if foo.status == 0:
        await custom_reply_command.send(foo.message)
    else:
        await custom_reply_command.send(foo.message)
    await custom_reply_command.finish()


@custom_reply_command.handle()
async def _(matcher: Matcher, bot: Bot, event: MessageEvent, args: Namespace = ShellCommandArgs()):
    action, func = await __func(bot, event, args)

    async def do_action():
        await func(args=args, bot=bot, event=event, matcher=matcher)
        await custom_reply_command.finish()

    if action in ["ls"]:
        if func is not None:
            await do_action()
        else:
            await custom_reply_command.send("未知错误")
        return
    elif action in ["add"]:
        # 进行参数校验
        for key, value in args.__dict__.items():
            if key in ["handle", "conv", "group", "message"]:
                continue
            if value is None:
                await custom_reply_command.finish(f"参数{key}未传入")
        return
    elif action in ["rm"]:
        # 直接执行
        await do_action()
        return
    else:
        await custom_reply_command.finish()


@custom_reply_command.got("message", prompt="请输入你要自定义的回复内容")
async def add(matcher: Matcher, bot: Bot, event: MessageEvent,
              message=Arg(),
              args: Namespace = ShellCommandArgs()):
    if args.handle != "add":
        return
    if message is None:
        await custom_reply_command.reject_arg("message", prompt="请输入你要自定义的回复")
    action, func = await __func(bot, event, args)
    if func is not None:
        await func(args=args, bot=bot, event=event, matcher=matcher)
        await custom_reply_command.finish()
    else:
        await custom_reply_command.send("未知错误")


@custom_reply_command.handle()
async def test(matcher: Matcher, bot: Bot, event: MessageEvent, args: Namespace = ShellCommandArgs()):
    if args.handl != "del":
        return
    await custom_reply_command.send("del cmd")
    action, func = await __func(bot, event, args)
    if func is not None:
        await func(args=args, bot=bot, event=event, matcher=matcher)
        await custom_reply_command.finish()
    else:
        await custom_reply_command.send("未知错误")
