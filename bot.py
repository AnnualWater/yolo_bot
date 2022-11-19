#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import datetime

import nonebot
from nonebot.adapters.onebot import V11Adapter

from nonebot.log import logger, default_format

now = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
logger.add(f"./data/log/{now}.log",
           rotation="00:00",
           diagnose=False,
           level="INFO",
           format=default_format)

nonebot.init()
app = nonebot.get_asgi()

driver = nonebot.get_driver()
driver.register_adapter(V11Adapter)

nonebot.load_from_json("plugin.json")

if __name__ == "__main__":
    # nonebot.logger.warning("Always use `nb run` to start the bot instead of manually running!")
    nonebot.run(app="__mp_main__:app")
