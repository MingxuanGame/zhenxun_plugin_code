from nonebot import on_command
from nonebot.adapters.onebot.v11 import Message, MessageEvent

from .data_source import run

__zx_plugin_name__ = "在线运行代码"
__plugin_usage__ = """
usage:
    在线运行代码
    指令：
        code [语言] [-i] [inputText]
        [代码]

        -i：可选 输入 后跟输入内容

    示例：
        运行代码示例(python)(无输入)：
            code py
                print("Hello World")
        运行代码示例(python)(有输入)：
            code py -i 你好
                print(input())

    目前仅支持c/cpp/c#/py/php/go/java/js
    运行于：https://glot.io/
""".strip()
__plugin_des__ = "在线运行c/py/go等代码"
__plugin_cmd__ = ["code [语言] -i [输入] [代码]"]
__plugin_settings__ = {
    "level": 5,
    "default_status": False,
    "limit_superuser": False,
    "cd": 10,
    "cmd": ["在线运行代码", "运行代码", "code"],
}
__plugin_version__ = 0.1
__plugin_author__ = "yzyyz"
__plugin_block_limit__ = {"rst": "代码正在润，请稍等"}
__plugin_cd_limit__ = {"cd": 10, "rst": "代码需要等一下才能润哦"}

runcode = on_command(
    "在线运行代码", priority=5, aliases={"运行代码", "code"}, block=True
)


@runcode.handle()
async def _(event: MessageEvent):
    code = str(event.get_message()).strip()
    res = await run(code)
    await runcode.send(message=Message(res), at_sender=True)
