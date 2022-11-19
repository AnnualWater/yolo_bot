# -*- coding: utf-8 -*-
# @Author:归年丶似水
# @Email:2448955276@qq.com
# @GitHub:github.com/AnnualWater

from nonebot.rule import ArgumentParser

crm_parser = ArgumentParser("crm")

crm_subparsers = crm_parser.add_subparsers(dest="handle")

# 列表操作
crm_list_parser = crm_subparsers.add_parser("ls", help="获取自定义回复列表")
list_group = crm_list_parser.add_argument_group()
list_group.add_argument("-g", "--group", type=int, help="群号，仅私聊有效")

# 添加操作
crm_add_parser = crm_subparsers.add_parser("add", help="添加自定义回复")
add_group = crm_add_parser.add_argument_group()
add_group.add_argument("-m", "--message", default=None, help="自定义的回复内容")
add_group.add_argument("-c", "--command", type=str, default=None, help="检测的关键字")
add_group.add_argument("-g", "--group", type=int, help="群号，仅私聊有效")
add_group.add_argument("-r", "--regex", type=bool, default=False, help="是否启用正则匹配")
add_group.add_argument("-t", "--type", type=str, default="group", help="回复的类型 private | group | group_private")

# 删除操作
crm_del_parser = crm_subparsers.add_parser("rm", help="删除自定义回复")
del_group = crm_del_parser.add_argument_group()
del_group.add_argument("-i", "--id", type=int, required=True, help="要删除的内容的ID")
