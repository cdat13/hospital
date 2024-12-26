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


class BaseModel(db.Model):
    __abstract__ = True

    id = Column(Integer, primary_key=True, autoincrement=True)

    def __str__(self):
        return self.name


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
    

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
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



        # u = User(name='admin', username='admin', password=str(hashlib.md5('123456'.encode('utf-8')).hexdigest()),
        #          user_role=UserRole.ADMIN)
        # db.session.add(u)
        # db.session.commit()
        #











