import os

libs = ["requests", "rich", "flask"]  # 罗列需要使用的库名称，避免因为没有第三方库报错

url = r"https://mirrors.tuna.tsinghua.edu.cn/pypi/web/simple/"  # 清华镜像网站
try:
    import requests
    from rich.console import Console
    from rich.progress import track
    from flask import (
        Flask,
        request,
        render_template,
        redirect,
        url_for,
        send_from_directory,
    )

    print("Input library successful")
except ModuleNotFoundError:
    print("Failed SomeHow")
    for lib in libs:
        print("Start install {0}".format(lib))
        os.system("pip install %s -i %s" % (lib, url))
        print("{0} install successful".format(lib))
    print("All install successful ")
import requests
from rich.console import Console
from rich.progress import track
from flask import (
    Flask,
    request,
    render_template,
    redirect,
    url_for,
    send_from_directory,
    make_response,
)
from rich.markdown import Markdown
import time
import json
import random

console = Console()
console.print("Welcome to [bold #6f42c1]WorldAI[/bold #6f42c1]")

with open("config.json", "r", encoding="utf-8") as f:
    config = json.loads(f.read())
    gpt = config["gpt"]

hichatlist = [
    "你好！我是WorldAI！🌍 很高兴能为你提供帮助！🤗请问有什么我可以帮助你的呢？✨",
    "你好！👋 我是WorldAI，很高兴为你服务！有什么问题我可以帮助你解答吗？😄",
    "你好！👋很高兴能为您提供帮助！有什么可以为您做的？",
    "你好！👋我是WorldAI，很高兴为您服务！如有任何问题，请随时告诉我。😊",
    "作为WorldAI，我可以帮助你回答各种问题，提供实用信息，玩一些小游戏，还可以聊天、分享笑话和格言等等。有什么问题或者需要帮助的话，尽管问我吧！😄",
    "Hi! 😄",
]

for i in gpt:
    gpt[i] = gpt[i] + "请使用HTML代码输出你的结果！换行要使用<br>！"
    print(gpt[i])

for step in track(range(100), description="读取配置文件..."):
    pass

# console.print(config)
console.print("UI by [bold #007bff]VariStyler[/bold #007bff]")

app = Flask(__name__)


@app.route("/")
def main():
    return render_template(
        "index.html", hichatlist=hichatlist[random.randint(0, len(hichatlist) - 1)]
    )


@app.route("/setting/cookie", methods=["POST"])
def setting_cookie():
    resp = make_response("success")
    if request.json.get("apikey") == "":
        resp.delete_cookie("apikey")
    else:
        resp.set_cookie("apikey", request.json.get("apikey"))

    if request.json.get("proxy") == "":
        resp.delete_cookie("proxy")
    else:
        resp.set_cookie("proxy", request.json.get("proxy"))
    return resp


@app.route("/setting")
def setting():
    if request.cookies.get("apikey"):
        apikey = request.cookies.get("apikey")
    else:
        apikey = ""

    if request.cookies.get("proxy"):
        proxy = request.cookies.get("proxy")
    else:
        proxy = ""
    return render_template("setting.html", apikey=apikey, proxy=proxy)


@app.route("/aigpt", methods=["POST"])
def aigpt():
    if request.cookies.get("apikey"):
        apikey = request.cookies.get("apikey")
    else:
        apikey = config["apikey"]

    if request.cookies.get("proxy"):
        proxy = request.cookies.get("proxy")
    else:
        proxy = "https://api.openai-proxy.com"
    headers = {"Content-Type": "application/json", "Authorization": "Bearer " + apikey}
    data = {
        "model": "gpt-3.5-turbo",
        "messages": [
            {"role": "system", "content": gpt[request.json.get("system")]},
            {"role": "user", "content": request.json.get("content")},
        ],
    }
    print(gpt[request.json.get("system")])
    returncon = requests.post(
        proxy + "/v1/chat/completions", json=data, headers=headers
    )
    return {
        "time": time.time(),
        "return": json.loads(returncon.text),
        "content": json.loads(returncon.text)["choices"][0]["message"]["content"],
        "data": request.json.get("content"),
    }


if __name__ == "__main__":
    app.run(host="192.168.3.129", port=8888, debug=True)
