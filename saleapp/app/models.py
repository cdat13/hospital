<<<<<<< HEAD
from email.policy import default
from xmlrpc.client import DateTime
from sqlalchemy.orm import relationship, backref
from sqlalchemy import Column, Integer, String, Float, Enum, ForeignKey, DateTime, false, column, Boolean, Date
from wtforms.validators import email

from app import db, app
from datetime import datetime
from enum import Enum as UserEnum
import random
import hashlib
from flask_login import UserMixin
=======
import random
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, Float, ForeignKey, Enum, DateTime
from app import db, app
from enum import Enum as RoleEnum
import hashlib
from flask_login import UserMixin
from datetime import datetime


class UserRole(RoleEnum):
    ADMIN = 1
    USER = 2


class User(db.Model, UserMixin):
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    username = Column(String(100), nullable=False, unique=True)
    password = Column(String(100), nullable=False)
    avatar = Column(String(100),
                    default="https://res.cloudinary.com/dxxwcby8l/image/upload/v1690528735/cg6clgelp8zjwlehqsst.jpg")
    user_role = Column(Enum(UserRole), default=UserRole.USER)
    receipts = relationship('Receipt', backref='user', lazy=True)
    comments = relationship('Comment', backref='user', lazy=True)
>>>>>>> 1ebfe801aae69c2bb0dad9335c5d444ca3c7ea13

class BaseModel(db.Model):
    __abstract__ = True

    id = Column(Integer, primary_key=True, autoincrement=True)

    def __str__(self):
        return self.name


<<<<<<< HEAD
class UserRole(UserEnum):
    ADMIN = 1
    USER = 2
    NURSE = 3
    DOCTOR = 4
    CASHIER = 5

class User(UserMixin, BaseModel):
    name = Column(String(50), nullable = False)
    username = Column(String(50), nullable= False, unique = True)
    password = Column(String(50), nullable= False)
    email = Column(String(50))
    active = Column(Boolean, default=True)
    joined_date = Column(DateTime, default=datetime.now())
    user_role = Column(Enum(UserRole), default = UserRole.USER)
    appointments = relationship('Appointment', backref='User', lazy=True)
    cashier = relationship('Cashier', backref='User', lazy=True)
    doctor = relationship('Doctor', backref='User', lazy=True)


class Doctor(BaseModel):
    salary = Column(Float, default=0)
    user_id = Column(Integer, ForeignKey(User.id), nullable=False)
    medical_report = relationship('MedicalReportDetails', backref='Doctor', lazy=True)


class Cashier(BaseModel):
    salary = Column(Float, default=0)
    user_id = Column(Integer, ForeignKey(User.id), nullable=False)
    bill = relationship('Bill', backref='Cashier', lazy=True)


class Appointment(BaseModel):
            name = Column(String(255), nullable=False)
            date = Column(Date(), nullable=False )
            department = Column(String(50))
            email = Column(String(50), nullable=False)
            phone = Column(String(10))
            address = Column(String(100))
            description= Column(String(100))
            status = Column(Boolean, default=False)
            user_id = Column(Integer, ForeignKey(User.id), nullable=False)
            medical_reports = relationship('MedicalReport', backref='Appointment', lazy=True)


class MedicalReport(BaseModel):
    diagnose = Column(String(255))
    created_date = Column(DateTime, default=datetime.now())
    details= relationship('MedicalReportDetails', backref='MedicalReport', lazy=True)
    appointment_id = Column(Integer, ForeignKey(Appointment.id), nullable=False)


class Medical(BaseModel):
    name = Column(String(255))
    price = Column(Float, default=0,  nullable=False)
    description = Column(String(255))
    details = relationship('MedicalReportDetails', backref='Medical', lazy=True)


class MedicalReportDetails(BaseModel):
    quantity = Column(Integer, default=0, nullable=False)
    unit_price = Column(Float, default=0,  nullable=False)
    medical_report_id = Column(Integer, ForeignKey(MedicalReport.id), nullable=False)
    medical_id = Column(Integer, ForeignKey(Medical.id), nullable=False)
    doctor_id = Column(Integer, ForeignKey(Doctor.id))


class Bill(BaseModel):
    total_price = Column(Float, default=0)
    created_date = Column(DateTime, default=datetime.now())
    user_id = Column(Integer, ForeignKey(User.id), nullable=False)
    cashier_id = Column(Integer, ForeignKey(Cashier.id))

=======
class Product(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False, unique=True)
    description = Column(String(255), nullable=True)
    price = Column(Float, default=0)
    image = Column(String(100), nullable=True)
    category_id = Column(Integer, ForeignKey(Category.id), nullable=False)
    details = relationship('ReceiptDetails', backref='product', lazy=True)
    comments = relationship('Comment', backref='product', lazy=True)

    def __str__(self):
        return self.name


class Receipt(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey(User.id), nullable=False)
    created_date = Column(DateTime, default=datetime.now())
    details = relationship('ReceiptDetails', backref='receipt', lazy=True)


class ReceiptDetails(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    product_id = Column(Integer, ForeignKey(Product.id), nullable=False)
    receipt_id = Column(Integer, ForeignKey(Receipt.id), nullable=False)
    quantity = Column(Integer, default=0)
    unit_price = Column(Float, default=0)


class Comment(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    content = Column(String(255), nullable=False)
    created_date = Column(DateTime, default=datetime.now())
    product_id = Column(Integer, ForeignKey(Product.id), nullable=False)
    user_id = Column(Integer, ForeignKey(User.id), nullable=False)
>>>>>>> 1ebfe801aae69c2bb0dad9335c5d444ca3c7ea13


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
<<<<<<< HEAD
        #
        #
        # u = User(name='doctor', username='doctor', password=str(hashlib.md5('1'.encode('utf-8')).hexdigest()),
        #          user_role=UserRole.DOCTOR)
        # db.session.add(u)
        m = Medical(name="ThuocA", description="Dung truoc khi an sang")
        n = Medical(name="ThuocB", description="Dung sau bua an")
        db.session.add(m)
        db.session.add(n)

        #
        # a = Appointment(name='admin',date='2024-2-14',department='Khoa noi', email='congdat@gmail.com', user_id = '1')
        # db.session.add(a)
=======



        # u = User(name='admin', username='admin', password=str(hashlib.md5('123456'.encode('utf-8')).hexdigest()),
        #          user_role=UserRole.ADMIN)
        # db.session.add(u)
        # db.session.commit()
        #
        # c1 = Category(name='Mobile')
        # c2 = Category(name='Tablet')
        # c3 = Category(name='Desktop')
        #
        # db.session.add_all([c1, c2, c3])
        # db.session.commit()
        #
        # data = [{
        #     "name": "iPhone 7 Plus",
        #     "description": "Apple, 32GB, RAM: 3GB, iOS13",
        #     "price": 17000000,
        #     "image": "https://res.cloudinary.com/dxxwcby8l/image/upload/v1688179242/hclq65mc6so7vdrbp7hz.jpg",
        #     "category_id": 1
        # }, {
        #     "name": "iPad Pro 2020",
        #     "description": "Apple, 128GB, RAM: 6GB",
        #     "price": 37000000,
        #     "image": "https://res.cloudinary.com/dxxwcby8l/image/upload/v1690528735/cg6clgelp8zjwlehqsst.jpg",
        #     "category_id": 2
        # }, {
        #     "name": "iPad Pro 2021",
        #     "description": "Apple, 128GB, RAM: 6GB",
        #     "price": 37000000,
        #     "image": "https://res.cloudinary.com/dxxwcby8l/image/upload/v1690528735/cg6clgelp8zjwlehqsst.jpg",
        #     "category_id": 2
        # }, {
        #     "name": "iPad Pro 2022",
        #     "description": "Apple, 128GB, RAM: 6GB",
        #     "price": 37000000,
        #     "image": "https://res.cloudinary.com/dxxwcby8l/image/upload/v1690528735/cg6clgelp8zjwlehqsst.jpg",
        #     "category_id": 2
        # }, {
        #     "name": "iPad Pro 2023",
        #     "description": "Apple, 128GB, RAM: 6GB",
        #     "price": 37000000,
        #     "image": "https://res.cloudinary.com/dxxwcby8l/image/upload/v1690528735/cg6clgelp8zjwlehqsst.jpg",
        #     "category_id": 2
        # }, {
        #     "name": "iPad Pro 2024",
        #     "description": "Apple, 128GB, RAM: 6GB",
        #     "price": 37000000,
        #     "image": "https://res.cloudinary.com/dxxwcby8l/image/upload/v1690528735/cg6clgelp8zjwlehqsst.jpg",
        #     "category_id": 2
        # }]
        #
        # for p in data:
        #     prod = Product(name=p['name'] + ' ' + str(random.randint(1, 100)), description=p['description'], price=p['price'],
        #                    image=p['image'], category_id=p['category_id'])
        #     db.session.add(prod)
        #
        # db.session.commit()

        c1 = Comment(content='good', product_id=1, user_id=1)
        c2 = Comment(content='nice', product_id=1, user_id=1)
        c3 = Comment(content='excellent', product_id=1, user_id=1)
        db.session.add_all([c1, c2, c3])
>>>>>>> 1ebfe801aae69c2bb0dad9335c5d444ca3c7ea13
        db.session.commit()












