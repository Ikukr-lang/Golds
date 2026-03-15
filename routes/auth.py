from flask import Blueprint, render_template, redirect, url_for, request, flash, session
from flask_login import login_user, logout_user, current_user
from models import db, User
import requests
import os

auth_bp = Blueprint('auth', __name__)

TOKEN = os.environ.get('TELEGRAM_GATEWAY_TOKEN')
BASE_URL = 'https://gatewayapi.telegram.org/'

def gateway_post(endpoint, json_data):
    headers = {
        'Authorization': f'Bearer {TOKEN}',
        'Content-Type': 'application/json'
    }
    r = requests.post(f"{BASE_URL}{endpoint}", headers=headers, json=json_data)
    if r.status_code == 200 and r.json().get('ok'):
        return r.json().get('result')
    else:
        print("Gateway error:", r.text)
        return None

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        phone = request.form.get('phone').strip()
        if not phone.startswith('+'):
            phone = '+' + phone
        
        # Отправляем код в Telegram
        data = {
            'phone_number': phone,
            'code_length': 6,
            'ttl': 180  # 3 минуты
        }
        result = gateway_post('sendVerificationMessage', data)
        
        if result and 'request_id' in result:
            session['request_id'] = result['request_id']
            session['phone'] = phone
            flash('Код отправлен в Telegram! Проверь чат «Verification Codes»')
            return redirect(url_for('auth.verify'))
        else:
            flash('Не удалось отправить код. Проверь номер или токен')
    return render_template('telegram_login.html')

@auth_bp.route('/verify', methods=['GET', 'POST'])
def verify():
    if 'request_id' not in session:
        return redirect(url_for('auth.login'))
    
    if request.method == 'POST':
        code = request.form.get('code').strip()
        request_id = session['request_id']
        phone = session['phone']
        
        # Проверяем код
        check_data = {
            'request_id': request_id,
            'code': code
        }
        result = gateway_post('checkVerificationStatus', check_data)
        
        if result and result.get('status') == 'code_valid':
            # Создаём/находим пользователя
            user = User.query.filter_by(phone=phone).first()
            if not user:
                user = User(phone=phone)
                db.session.add(user)
                db.session.commit()
            
            login_user(user)
            session.pop('request_id', None)
            session.pop('phone', None)
            flash('Вход выполнен!')
            return redirect(url_for('dashboard.index'))
        else:
            flash('Неверный код')
    
    return render_template('verify_code.html')

@auth_bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('public.index'))
