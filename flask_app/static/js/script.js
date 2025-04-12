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

// 添加收藏功能
function addToFavorites(productId) {
    fetch('/add_favorite', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: `product_id=${encodeURIComponent(productId)}`
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === 'success') {
            alert('已添加到收藏');
        } else {
            alert(data.message || '添加收藏失败');
        }
    });
}

// 创建订单
function createOrder(productId, sellerId, price) {
    // 这里应该弹出表单收集支付方式和收货地址
    const paymentMethod = prompt('请输入支付方式 (支付宝/微信/银行卡):');
    if (!paymentMethod) return;
    
    const shippingAddress = prompt('请输入收货地址:');
    if (!shippingAddress) return;
    
    fetch('/create_order', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: `product_id=${encodeURIComponent(productId)}&seller_id=${encodeURIComponent(sellerId)}&price=${encodeURIComponent(price)}&payment_method=${encodeURIComponent(paymentMethod)}&shipping_address=${encodeURIComponent(shippingAddress)}`
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === 'success') {
            alert('订单创建成功');
            window.location.href = '/orders';
        } else {
            alert(data.message || '创建订单失败');
        }
    });
}