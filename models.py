import os
from sqlalchemy import Column, String, Integer, create_engine
from flask_sqlalchemy import SQLAlchemy
import json


# DB_HOST = os.getenv('DB_HOST', '127.0.0.1:5432')
# DB_USER = os.getenv('DB_USER', 'postgres')
#DB_PASSWORD = os.getenv('DB_PASSWORD', '111')
# DB_NAME = os.getenv('DB_NAME', 'hospital')
# database_path = 'postgresql+psycopg2://{}:{}@{}/{}'.format(
#     DB_USER, DB_PASSWORD, DB_HOST, DB_NAME)
database_name = 'hospital'
#database_path = "postgres://:{}/{}".format(DB_PASSWORD, database_name)
database_path = os.environ['DATABASE_URL']
db = SQLAlchemy()


'''
setup_db(app)
    binds a flask application and a SQLAlchemy service
'''


def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    db.create_all()


'''
Extend the base Model class to add common methods
'''


class IDU(db.Model):
    __abstract__ = True

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self):
        db.session.commit()


'''
Doctor

'''

# HOSPITAL MANAGEMENT SYSTEM DATABASE PROJECT


class Doctor(IDU):
    __tablename__ = 'doctor'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    deparment = Column(String)
    level = Column(String)

    def __init__(self, name, deparment, level):
        self.name = name
        self.deparment = deparment
        self.level = level

    def format(self):
        return {
            'id': self.id,
            'name': self.name,
            'deparment': self.deparment,
            'level': self.level
        }


'''
Patient

'''


class Patient(IDU):
    __tablename__ = 'patient'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    age = Column(Integer)
    gender = Column(String)
    doctor_id = db.Column(db.Integer, db.ForeignKey(
        'doctor.id', ondelete="CASCADE"))
    date_of_appointment = db.Column(db.DateTime())

    def __init__(self, name, age, gender, doctor_id, date_of_appointment):
        self.name = name
        self.age = age
        self.gender = gender
        self.doctor_id = doctor_id
        self.date_of_appointment = date_of_appointment

    def format(self):
        return {
            'id': self.id,
            'name': self.name,
            'age': self.age,
            'gender': self.gender,
            'doctor_id': self.doctor_id,
            'date_of_appointment': self.date_of_appointment
        }
