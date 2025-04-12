import sqlite3
import random
import hashlib
from datetime import datetime, timedelta
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
    favorites = [
        {
            "favorite_id": 1,
            "user_id": 1,
            "product_id": 1,
            "add_date": datetime(2024, 11, 3, 14, 30)
        },
        {
            "favorite_id": 2,
            "user_id": 2,
            "product_id": 3,
            "add_date": datetime(2024, 11, 5, 9, 15)
        },
        {
            "favorite_id": 3,
            "user_id": 1,
            "product_id": 2,
            "add_date": datetime(2024, 11, 6, 18, 50)
        },
        {
            "favorite_id": 4,
            "user_id": 3,
            "product_id": 4,
            "add_date": datetime(2024, 11, 7, 11, 10)
        },
        {
            "favorite_id": 5,
            "user_id": 4,
            "product_id": 5,
            "add_date": datetime(2024, 11, 8, 20, 5)
        }
    ]  # 实际应从数据库查询
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

# 模拟数据
def generate_products():
    conditions = ['new', 'like new', 'good', 'fair', 'poor']
    statuses = ['available', 'reserved', 'sold', 'removed']
    locations = ['北京', '上海', '广州', '深圳', '杭州']

    products = []
    for i in range(1, 11):
        original_price = round(random.uniform(100, 1000), 2)
        discount = random.uniform(0.5, 0.9)
        price = round(original_price * discount, 2)
        condition = random.choice(conditions)
        status = random.choice(statuses)
        product = {
            'id': i,
            'seller_id': random.randint(1, 5),
            'title': f'商品{i}',
            'description': f'这是商品{i}的描述信息',
            'price': price,
            'original_price': original_price,
            'condition': condition,
            'condition_display': {
                'new': '全新',
                'like new': '几乎全新',
                'good': '良好',
                'fair': '一般',
                'poor': '较差'
            }[condition],
            'location': random.choice(locations),
            'post_date': datetime.now() - timedelta(days=random.randint(1, 30)),
            'status': status,
            'view_count': random.randint(10, 200),
            'fav_count': random.randint(0, 50)
        }
        products.append(product)
    return products

@app.route('/products')
def product_list():
    search = request.args.get('search', '')
    condition = request.args.get('condition', '')
    status = request.args.get('status', 'available')
    sort = request.args.get('sort', 'newest')
    page = int(request.args.get('page', 1))
    per_page = 5

    # 获取全部数据并做简单过滤
    all_products = generate_products()

    # 搜索过滤
    if search:
        all_products = [p for p in all_products if search in p['title']]

    if condition:
        all_products = [p for p in all_products if p['condition'] == condition]

    if status != 'all':
        all_products = [p for p in all_products if p['status'] == status]

    # 排序
    if sort == 'newest':
        all_products.sort(key=lambda x: x['post_date'], reverse=True)
    elif sort == 'price_low':
        all_products.sort(key=lambda x: x['price'])
    elif sort == 'price_high':
        all_products.sort(key=lambda x: x['price'], reverse=True)
    elif sort == 'popular':
        all_products.sort(key=lambda x: x['view_count'], reverse=True)

    # 分页
    total = len(all_products)
    pages = (total + per_page - 1) // per_page
    products = all_products[(page - 1) * per_page : page * per_page]

    return render_template('product_list.html', products=products, page=page, pages=pages)

if __name__ == '__main__':
    app.run(debug=True)