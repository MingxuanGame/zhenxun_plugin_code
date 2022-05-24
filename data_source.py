import re

from nonebot.log import logger

from utils.http_utils import AsyncHttpx

codeType = {
    "py": ["python", "py"],
    "cpp": ["cpp", "cpp"],
    "java": ["java", "java"],
    "php": ["php", "php"],
    "js": ["javascript", "js"],
    "c": ["c", "c"],
    "c#": ["csharp", "cs"],
    "go": ["go", "go"],
    "asm": ["assembly", "asm"],
}


async def run(code):
    code = code.replace("&amp;", "&").replace("&#91;", "[").replace("&#93;", "]")
    try:
        cmd = re.findall(
            r"(py|php|java|cpp|js|c#|c|go|asm)\s?(-i)?\s?(\w*)" r"?(\n|\r)((?:.|\n)+)",
            code,
        )[0]
        logger.info(f"command: {cmd}")
    except Exception:
        return "输入有误汪\n目前仅支持c/cpp/c#/py/php/go/java/js"
    lang, code = cmd[0], cmd[4]
    stdin = cmd[2] if "-i" in cmd else ""
    data = {
        "files": [{"name": f"main.{codeType[lang][1]}", "content": code}],
        "stdin": stdin,
        "command": "",
    }
    headers = {
        "Authorization": "Token 0123456-789a-bcde-f012-3456789abcde",
        "content-type": "application/",
    }
    response = await AsyncHttpx.post(
        url=f"https://glot.io/run/{codeType[lang][0]}?version=latest",
        headers=headers,
        json=data,
    )
    print(data)
    if response.status_code == 200:
        if response.json()["stdout"] == "":
            return response.json()["stderr"].strip()
        if len(repr(response.json()["stdout"])) < 100:
            return response.json()["stdout"]
        else:
            return "返回字符过长呐~~~"
