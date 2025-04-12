import sqlite3
import random
import hashlib
from datetime import datetime
import faker

from flask import Flask, render_template, request, redirect, url_for

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

def insert_message(user_id, product_id, add_date):
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

app = Flask(__name__)

users = []
messages = []
orders = []
favorites = []

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/home')
def home():
    return render_template('base.html')

@app.route('/order_management')
def order_management():
    return render_template('order_management.html', orders=orders)

@app.route('/favorites')
def favorites_page():
    return render_template('favorites.html', favorites=favorites)

if __name__ == '__main__':
    app.run(debug=True)