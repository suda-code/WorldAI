function AiGo() {
    var div = document.getElementById("div"),
        system = document.getElementById("system"),
        textarea = document.getElementById("textarea");
        div.style = "display: flex; justify-content: center; align-items: center;width: 100%;height: 300px;"
        div.innerHTML = `<div class="loader">
        <div class="square" id="sq1"></div>
        <div class="square" id="sq2"></div>
        <div class="square" id="sq3"></div>
        <div class="square" id="sq4"></div>
        <div class="square" id="sq5"></div>
        <div class="square" id="sq6"></div>
        <div class="square" id="sq7"></div>
        <div class="square" id="sq8"></div>
        <div class="square" id="sq9"></div>
      </div>`
    $.ajax({
        type: "POST",
        url: "/aigpt",
        contentType: "application/json; charset=utf-8",
        // headers: {
        //     Accept: "application/json; charset=utf-8"
        // },
        data: JSON.stringify({   // 将数据转换为 JSON 字符串
            system: system.value,
            content: textarea.value
        }),
        success: function (result) {    // 回调函数
            try {
                div.innerHTML = result["content"];
            }
            catch {
                console.log("解池错误");
            }
        },
        error: function(XMLHttpRequest, textStatus, errorThrown) {
            try {
                div.innerHTML = `<b style="color: red;">Error!</b> ApiKey or Proxy is wrong`;
            }
            catch {
                console.log("解池错误");
            }
        },
    }
    )
    textarea.value = ""
    div.style = "width: 100%;height: auto;"
}

document.onkeydown = function (e) {
    var keyCode = e.key;
    if (!e.shiftKey && keyCode === 'Enter') {
        AiGo()
    };
}

document.getElementById("send").onclick = () => {
    AiGo()
}