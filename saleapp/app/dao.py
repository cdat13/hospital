
from datetime import datetime
import mysql.connector
from flask_login import current_user
from app import app, db
from app.models import User, Appointment, UserRole, Medical, MedicalReport, MedicalReportDetails
import hashlib

from app.models import Category, Product, User, Receipt, ReceiptDetails, Comment
from app import app, db
import hashlib
import cloudinary.uploader
from flask_login import current_user
from sqlalchemy import func
from datetime import datetime



def auth_user(username, password, role=None):
    password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())

    u = User.query.filter(User.username.__eq__(username.strip()),
                             User.password.__eq__(password))

    if role:
        u = u.filter(User.user_role.__eq__(role))

    return u.first()



def auth_staff(role):
    if role.__eq__('DOCTOR'):
        if User.user_role.__eq__(role):
            return True
        else: return False

def load_products(kw=None, category_id=None, page=1):
    products = Product.query
>>>>>>> 1ebfe801aae69c2bb0dad9335c5d444ca3c7ea13

def add_user(name, username, password, email, phone):
    password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())
    user = User(name=name, username=username, password=password, email = email)     # type: ignore

    db.session.add(user)
    db.session.commit()


def count_appointment(date):
    python_date = datetime.strptime(date, "%Y-%m-%d").date()
    if Appointment.query.filter(Appointment.date == date).count() < 2:
        return True
    else:
        return False


def add_appointment(name, email, phone, address, department, description, date):

    appointment = Appointment(name = name, email = email, phone = phone, address = address, date = date,
                              department = department, description = description, user_id=current_user.id)
    db.session.add(appointment)
    db.session.commit()


def get_user_by_id(id):
    return User.query.get(id)


def get_user_by_role(id):
    return User.query.get(User.user_role)


def get_appointment_by_id(appointment_id):
    return Appointment.query.get(appointment_id)


def load_appointment(kw=None, date=None, page=1, status=None):
    appointments = Appointment.query
    if kw:
        appointments = appointments.filter(Appointment.name.contains(kw))
    if date:
        appointments = appointments.filter(Appointment.date == date)
    if status:
        appointments = appointments.filter(Appointment.status == True)

    page_size = app.config["PAGE_SIZE"]
    start = (page - 1) * page_size
    appointments = appointments.slice(start, start + page_size)

    return appointments.all()


def load_medical(kw=None,  page=1):
    medicals = Medical.query
    if kw:
        medicals = medicals.filter(Medical.name.contains(kw))

    page_size = app.config["PAGE_SIZE"]
    start = (page - 1) * page_size
    medicals = medicals.slice(start, start + page_size)

    return medicals.all()


def update_appointment(date):
    conn=mysql.connector.connect(host="localhost",user="root", password="Admin123@", database="hospital")
    my_cursor = conn.cursor()
    my_cursor.execute("update Appointment SET status = TRUE WHERE status = FALSE")
    conn.commit()
    conn.disconnect()


def count_app_nurse():
    return Appointment.query.count()


def count_cart(cart):
    total_quantity= 0

    if cart:
        for c in cart.values():
            total_quantity += c['quantity']
    return {
        'total_quantity': total_quantity,
    }


def add_report(cart, appointment_id):
    if cart:
        report = MedicalReport(appointment_id=appointment_id)
        db.session.add(report)

        for c in cart.values():
            d = MedicalReportDetails(MedicalReport = report,
                                     medical_id=c['id'],
                                     quantity=c['quantity'])
            db.session.add(d)
        db.session.commit()

    if category_id:
        products = products.filter(Product.category_id == category_id)

    page_size = app.config["PAGE_SIZE"]
    start = (page - 1) * page_size
    products = products.slice(start, start + page_size)

    return products.all()


def count_products():
    return Product.query.count()


def auth_user(username, password, role=None):
    password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())

    u = User.query.filter(User.username.__eq__(username.strip()),
                          User.password.__eq__(password))
    if role:
        u = u.filter(User.user_role.__eq__(role))

    return u.first()


def add_user(name, username, password, avatar):
    password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())

    u = User(name=name, username=username, password=password,
             avatar='https://res.cloudinary.com/dxxwcby8l/image/upload/v1690528735/cg6clgelp8zjwlehqsst.jpg')

    if avatar:
        res = cloudinary.uploader.upload(avatar)
        u.avatar = res.get('secure_url')

    db.session.add(u)
    db.session.commit()


def add_receipt(cart):
    if cart:
        r = Receipt(user=current_user)
        db.session.add(r)

        for c in cart.values():
            d = ReceiptDetails(quantity=c['quantity'], unit_price=c['price'],
                               product_id=c['id'], receipt=r)
            db.session.add(d)

        db.session.commit()


def get_user_by_id(id):
    return User.query.get(id)


def revenue_stats(kw=None):
    query = db.session.query(Product.id, Product.name, func.sum(ReceiptDetails.quantity * ReceiptDetails.unit_price))\
                      .join(ReceiptDetails, ReceiptDetails.product_id.__eq__(Product.id)).group_by(Product.id)

    if kw:
        query = query.filter(Product.name.contains(kw))

    return query.all()


def period_stats(p='month', year=datetime.now().year):
    return db.session.query(func.extract(p, Receipt.created_date),
                            func.sum(ReceiptDetails.quantity * ReceiptDetails.unit_price))\
                      .join(ReceiptDetails, ReceiptDetails.receipt_id.__eq__(Receipt.id))\
                      .group_by(func.extract(p, Receipt.created_date), func.extract('year', Receipt.created_date))\
                      .filter(func.extract('year', Receipt.created_date).__eq__(year)).all()


def stats_products():
    return db.session.query(Category.id, Category.name, func.count(Product.id))\
        .join(Product, Product.category_id.__eq__(Category.id), isouter=True).group_by(Category.id).all()


def get_prod_by_id(id):
    return Product.query.get(id)


def load_comments(product_id):
    return Comment.query.filter(Comment.product_id.__eq__(product_id))


def add_comment(content, product_id):
    c = Comment(content=content, product_id=product_id, user=current_user)
    db.session.add(c)
    db.session.commit()

    return c


if __name__ == '__main__':
    with app.app_context():
        print(count_products())
>>>>>>> 1ebfe801aae69c2bb0dad9335c5d444ca3c7ea13
