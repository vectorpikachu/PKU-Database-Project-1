import sqlite3
import random
import hashlib
from datetime import datetime
import faker

from flask import Flask, flash, render_template, request, redirect, url_for, session, jsonify

db_path = 'xianyu.db'

def insert_user(username, password, phone, email, credit_score, registration_date, last_login, status):
    try:
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO User (username, password_hash, phone, email, credit_score, registration_date, last_login, status)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (username, password, phone, email, credit_score, registration_date, last_login, status))
            conn.commit()
            return "success"
    except:
        conn.rollback()
        return "fail"

def insert_order(product_id, buyer_id, seller_id, price, status, payment_method, shipping_address, tracking_number):
    try:
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO Order_ (product_id, buyer_id, seller_id, order_date, price, status, payment_method, shipping_address, tracking_number)
                VALUES (?, ?, ?, datetime('now'), ?, ?, ?, ?, ?)
            ''', (product_id, buyer_id, seller_id, price, status, payment_method, shipping_address, tracking_number))
            conn.commit()
            return "success"
    except:
        conn.rollback()
        return "fail"

def insert_message(sender_id, receiver_id, product_id, content, send_time, is_read):
    try:
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO Message (sender_id, receiver_id, product_id, content, send_time, is_read)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (sender_id, receiver_id, product_id, content, send_time, is_read))
            conn.commit()
            return "success"
    except:
        conn.rollback()
        return "fail"

def insert_favorite(user_id, product_id, add_date):
    try:
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT OR IGNORE INTO Favorite (user_id, product_id, add_date)
                VALUES (?, ?, ?)
            ''', (user_id, product_id, add_date))
            conn.commit()
            return "success"
    except:
        conn.rollback()
        return "fail"

def delete_favorite(user_id, product_id):
    raise NotImplementedError

app = Flask(__name__)
app.secret_key = 'a9d8s7f6g5h4j3k2l1!@#secret_key_for_session$%^&*'

users = []
messages = []
orders = []
favorites = []

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # 在这里验证账号密码（例如查数据库）
        if username == 'test' and password == '123':
            session['username'] = username  # 设置登录状态
            session['user_id'] = 1  # 假设用户ID为1
            flash('登录成功！', 'success')
            return redirect(url_for('home'))  # 登录成功后跳转
        else:
            flash('用户名或密码错误', 'danger')
            return redirect(url_for('login'))
    
    return render_template('login.html')  # GET 请求返回登录页面

@app.route('/logout')
def logout():
    session.pop('username', None)
    flash('已成功登出', 'info')
    return redirect(url_for('home'))

from datetime import datetime
import hashlib

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        raw_password = request.form['password']
        phone = request.form['phone']
        email = request.form['email']

        # 密码加密
        password_hash = hashlib.sha256(raw_password.encode()).hexdigest()

        # 注册时间、上次登录时间
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        credit_score = 100  # 默认信用分
        status = 'active'   # 默认状态

        insert_user(
            username=username,
            password=password_hash,
            phone=phone,
            email=email,
            credit_score=credit_score,
            registration_date=now,
            last_login=now,
            status=status
        )

        flash('注册成功！请登录', 'success')
        return redirect(url_for('login'))

    return render_template('register.html')



@app.route('/messages')
def message_system():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    user_id = session['user_id']
    # 这里应该从数据库获取用户的消息列表，简化示例
    messages = []  # 实际应从数据库查询
    return render_template('message_system.html', messages=messages)

@app.route('/send_message', methods=['POST'])
def send_message():
    if 'user_id' not in session:
        return jsonify({'status': 'fail', 'message': '请先登录'})
    
    sender_id = session['user_id']
    receiver_id = request.form.get('receiver_id')
    product_id = request.form.get('product_id')
    content = request.form.get('content')
    send_time = datetime.now()
    
    result = insert_message(sender_id, receiver_id, product_id, content, send_time, False)
    if result == "success":
        return jsonify({'status': 'success'})
    else:
        return jsonify({'status': 'fail', 'message': '发送失败'})

@app.route('/orders')
def order_management():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    user_id = session['user_id']
    # 这里应该从数据库获取用户的订单列表，简化示例
    orders = []  # 实际应从数据库查询
    return render_template('order_management.html', orders=orders)

@app.route('/create_order', methods=['POST'])
def create_order():
    if 'user_id' not in session:
        return jsonify({'status': 'fail', 'message': '请先登录'})
    
    product_id = request.form.get('product_id')
    buyer_id = session['user_id']
    seller_id = request.form.get('seller_id')
    price = request.form.get('price')
    status = "pending"
    payment_method = request.form.get('payment_method')
    shipping_address = request.form.get('shipping_address')
    tracking_number = ""
    
    result = insert_order(product_id, buyer_id, seller_id, price, status, payment_method, shipping_address, tracking_number)
    if result == "success":
        return jsonify({'status': 'success'})
    else:
        return jsonify({'status': 'fail', 'message': '创建订单失败'})

@app.route('/favorites')
def favorites():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    user_id = session['user_id']
    # 这里应该从数据库获取用户的收藏列表，简化示例
    favorites = []  # 实际应从数据库查询
    return render_template('favorites.html', favorites=favorites)

@app.route('/add_favorite', methods=['POST'])
def add_favorite():
    if 'user_id' not in session:
        return jsonify({'status': 'fail', 'message': '请先登录'})
    
    user_id = session['user_id']
    product_id = request.form.get('product_id')
    add_date = datetime.now()
    
    result = insert_favorite(user_id, product_id, add_date)
    if result == "success":
        return jsonify({'status': 'success'})
    else:
        return jsonify({'status': 'fail', 'message': '添加收藏失败'})

@app.route('/remove_favorite', methods=['POST'])
def remove_favorite():
    if 'user_id' not in session:
        return jsonify({'status': 'fail', 'message': '请先登录'})
    
    user_id = session['user_id']
    product_id = request.form.get('product_id')
    
    result = delete_favorite(user_id, product_id)  # 需要实现这个函数
    if result == "success":
        return jsonify({'status': 'success'})
    else:
        return jsonify({'status': 'fail', 'message': '移除收藏失败'})

if __name__ == '__main__':
    app.run(debug=True)