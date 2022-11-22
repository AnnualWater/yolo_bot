from pathlib import Path

import nonebot
from nonebot import require, on_message

require("yolo_money")

test = on_message()


@test.handle()
async def _():
    pass


_sub_plugins = set()
_sub_plugins |= nonebot.load_plugins(
    str((Path(__file__).parent / "plugins").
        resolve()))
