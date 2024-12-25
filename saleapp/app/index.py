from datetime import datetime
import flask_login
from flask import render_template, request, redirect, url_for, session, jsonify
from wtforms.validators import email
import math
import dao
from app import app, login
from flask_login import login_user, logout_user, login_required, current_user
from app.dao import add_appointment, count_appointment, get_user_by_role, update_appointment, get_appointment_by_id
from app.models import db, User, UserRole
from flask_admin import Admin


@app.route("/")
def index():
    return render_template('layout/index.html')


@app.route('/register', methods=['get', 'post'])
def register_user():
    err_msg = ''
    if request.method.__eq__('POST'):
        password = request.form.get('password')
        confirm = request.form.get('confirm')

        if password.__eq__(confirm):
            data = request.form.copy()
            del data['confirm']
            #
            # avatar = request.files.get('avatar')
            # dao.add_user(avatar=avatar, **data)
            dao.add_user(**data)
            return redirect(url_for('index'))
        else:
            err_msg = 'Mật khẩu không khớp!'

    return render_template('layout/register.html', err_msg=err_msg)


@app.route('/login', methods=['get','post'])
def login_process():
    err_msg = ''
    if request.method.__eq__('POST'):
        username = request.form.get('username')
        password = request.form.get('password')

        u = dao.auth_user(username=username, password=password, role=UserRole.USER)
        if u:
            login_user(u)
            return redirect('/')
        else:
            err_msg = 'Sai tên đăng nhập hoặc mật khẩu!'

    return render_template('layout/login.html', err_msg=err_msg)


@app.route('/login_admin', methods=['post'])
def login_admin():
        username = request.form.get('username')
        password = request.form.get('password')

        u = dao.auth_user(username=username, password=password, role = UserRole.ADMIN )
        if u:
            login_user(u)

        return redirect('/admin')


@app.route('/user-logout')
def logout_process():
    logout_user()
    return redirect('/login')


@login.user_loader
def load_user(user_id):
    return dao.get_user_by_id(user_id)


@app.route('/appointment', methods=['get','post'])
@login_required
def make_appointment():
    err_msg= ''
    if request.method.__eq__('POST'):
        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        address = request.form.get('address')
        department = request.form.get('department')
        description = request.form.get('description')
        date = request.form.get('date')
        if count_appointment(date):
            dao.add_appointment(name=name, email=email, phone=phone,address=address, date = date,
                            department=department, description=description)
            return redirect(url_for('index'))
        else:
            err_msg = 'Số lượng bệnh nhân ngày đó đã quá tải!'
    return render_template('layout/appointment.html', err_msg=err_msg)


@app.route('/nurse', methods= ['get','post'])
@login_required
def nurse():
    err_msg=''
    if  current_user.user_role.__eq__(UserRole.NURSE):
        kw = request.args.get('kw')
        date = request.form.get('date')
        page = request.args.get('page', 1)
        apps = dao.load_appointment(kw=kw, date=date, page=int(page))
        total = dao.count_app_nurse()
        return render_template('layout/nurse.html', appointments=apps,
                                   pages=math.ceil(total / app.config["PAGE_SIZE"]))
    else:
        err_msg ='Ban khong co quyen truy cap'
        return render_template('layout/login_staff.html', err_msg=err_msg)


@app.route('/nurse_update', methods= ['get','post'])
@login_required
def nurse_update():
    if request.method.__eq__("POST"):
        date = request.form.get('date')
        update_appointment(date)
    return redirect('/nurse')


@app.route('/login_staff', methods=['get','post'])
def login_process_staff():
    err_msg = ''
    if request.method.__eq__('POST'):
        username = request.form.get('username_staff')
        password = request.form.get('password_staff')
        role = request.form.get('role')
        u = dao.auth_user(username=username, password=password)
        if u:
            login_user(u)
            return redirect('/nurse')
        else:
            err_msg = 'Sai tên đăng nhập hoặc mật khẩu!'

    return render_template('layout/login_staff.html', err_msg=err_msg)


@app.route('/doctor_main', methods=['get','post'])
@login_required
def doctor_main():
    if current_user.is_authenticated and current_user.user_role.__eq__(UserRole.DOCTOR):
        kw = request.args.get('kw')
        date = datetime.now().date()
        page = request.args.get('page', 1)
        apps = dao.load_appointment(kw=kw, date=date, page=int(page), status=True)
        total = dao.count_app_nurse()
        return render_template('layout/doctor_main.html', appointments=apps,
                               pages=math.ceil(total / app.config["PAGE_SIZE"]))
    else:
        err_msg = 'Ban khong co quyen truy cap'
        return render_template('layout/login_staff.html', err_msg=err_msg)


@app.route('/doctor/<int:appointment_id>', methods=['get','post'])
@login_required
def doctor(appointment_id):
    err_msg=''
    appointment = dao.get_appointment_by_id(appointment_id)
    if current_user.is_authenticated and current_user.user_role.__eq__(UserRole.DOCTOR):
        kw = request.args.get('kw')
        page = request.args.get('page', 1)
        m = dao.load_medical(kw=kw, page=int(page))
        total = dao.count_app_nurse()
        return render_template('layout/doctor.html', medicals=m,
                               pages=math.ceil(total / app.config["PAGE_SIZE"]))
    else:
        err_msg='Ban khong co quyen truy cap'

    return render_template('layout/login_staff.html', err_msg=err_msg)


@app.route('/doctor', methods   =['post','get'])
def doctor2():
    return redirect('/doctor_main')


@app.route('/api/add-report', methods=['post'])
def add_report():
    data = request.json
    appointment_id = data.get('appointment_id')
    try:
        dao.add_report(session.get('cart'), appointment_id)
    except Exception as ex:
        return jsonify({'code':400})
    else:
        del session['cart']

    return jsonify({'code': 200})




@app.route( '/api/medical_report', methods=['get','post'])
def medical_report():
    data = request.json
    id= str(data.get('id'))
    name=str(data.get('name'))
    description=data.get('description')

    cart = session.get('cart')
    if not cart:
        cart = {}
    if id in cart:
        cart[id]['quantity'] = cart[id]['quantity'] + 1
    else:
        cart[id] = {
            'id': id,
            'name': name,
            'description': description,
            'quantity': 1,
        }
    session['cart'] = cart

    return jsonify(dao.count_cart(cart))


@app.context_processor
def common_response():
    return {'cart_stats': dao.count_cart(session.get('cart')) }


@app.route('/api/update-cart', methods=['put'])
def update_cart():
    data =request.json
    id = str(data.get('id'))
    quantity = data.get('quantity')

    # quantity = request.json.get('quantity', 0)

    cart = session.get('cart')
    if cart and id in cart:
        cart[id]['quantity'] = quantity
        session['cart'] = cart

    return jsonify(dao.count_cart(cart))


@app.route('/api/delete-cart/<int:appointment_id>', methods=['delete'])
def delete_cart(appointment_id):
    cart = session.get('cart')

    if cart and appointment_id in cart:
        del cart[appointment_id]

    session['cart'] = cart


    return jsonify(dao.count_cart(cart))


if __name__ == '__main__':
    from app import admin
    with app.app_context():
        app.run(debug=True)
