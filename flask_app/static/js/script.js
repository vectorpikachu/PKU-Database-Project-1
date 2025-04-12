// script.js

document.addEventListener("DOMContentLoaded", function () {
    console.log("页面加载完成");

    const buyButtons = document.querySelectorAll("form[action*='purchase'] button");

    buyButtons.forEach(button => {
        button.addEventListener("click", function (e) {
            const confirmed = confirm("确认要购买该商品吗？");
            if (!confirmed) {
                e.preventDefault();
            }
        });
    });

    const messageForm = document.querySelector("form[action*='send_message']");
    if (messageForm) {
        messageForm.addEventListener("submit", function (e) {
            const msg = document.getElementById("message_text").value;
            if (!msg.trim()) {
                alert("请输入消息内容！");
                e.preventDefault();
            }
        });
    }
});
