from . import db
from flask_login import UserMixin


class User(db.Model, UserMixin):

    id = db.Column(db.Integer, primary_key = True)
    email = db.Column(db.String(150), unique = True)
    name = db.Column(db.String(150), unique = True)
    password = db.Column(db.String(150))


class Batch(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(50), unique = True)
    sunday = db.Column(db.String(50), unique = True)
    monday = db.Column(db.String(50), unique = True)
    tuesday = db.Column(db.String(50), unique = True)
    wednesday = db.Column(db.String(50), unique = True)
    thursday = db.Column(db.String(50), unique = True)
    friday = db.Column(db.String(50), unique = True)
    saturday = db.Column(db.String(50), unique = True)
    students = db.relationship('Student', backref='batch')


class Student(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(150))
    phone = db.Column(db.Integer)
    email = db.Column(db.String(150))
    school = db.Column(db.String(50))
    dob = db.Column(db.Date)
    batch_id = db.Column(db.Integer, db.ForeignKey('batch.id', onupdate='CASCADE'))


class Alumini(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(150))
    phone = db.Column(db.Integer)
    email = db.Column(db.String(150))
    school = db.Column(db.String(50))
    dob = db.Column(db.Date)
