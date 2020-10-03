from flask_login import UserMixin

from reggio import db, login_manager


class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True, unique=True)
    username = db.Column(db.String(80), nullable=False, unique=True)
    email = db.Column(db.String(120), nullable=False, unique=True)
    userType = db.Column(db.String(80), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    name = db.Column(db.String(120))
    surname = db.Column(db.String(120))
    phone = db.Column(db.String(13))
    viber = db.Column(db.String(255))
    avatar = db.Column(db.String(255))

class Child(db.Model):
    __tablename__ = 'child'
    id = db.Column(db.Integer, primary_key=True, unique=True)
    username = db.Column(db.String(80), nullable=False)
    avatar = db.Column(db.String(255))
    name = db.Column(db.String(120))
    surname = db.Column(db.String(120))
    parents = db.Column(db.String(120))

class Parent(db.Model):
    __tablename__ = 'parent'
    id = db.Column(db.Integer, primary_key=True, unique=True)
    username = db.Column(db.String(80), nullable=False)
    avatar = db.Column(db.String(255))
    name = db.Column(db.String(120))
    surname = db.Column(db.String(120))
    children = db.Column(db.String(120))

class Teacher(db.Model):
    __tablename__ = 'teacher'
    id = db.Column(db.Integer, primary_key=True, unique=True)
    username = db.Column(db.String(80), nullable=False)
    avatar = db.Column(db.String(255))
    name = db.Column(db.String(120))
    surname = db.Column(db.String(120))

class IndividualClass(db.Model):
    __tablename__ = 'individualClass'
    id = db.Column(db.Integer, primary_key=True, unique=True)
    teacherUsername = db.Column(db.String(255), nullable=False)
    teacherName = db.Column(db.String(255))
    studentUsername = db.Column(db.String(255), nullable=False)
    studentName = db.Column(db.String(255))
    timeSpent = db.Column(db.Integer)
    creationDate = db.Column(db.DateTime, server_default=db.func.now())
    lessonDate = db.Column(db.DateTime)
    comment = db.Column(db.String(1028))
    grade = db.Column(db.Integer)
    topic = db.Column(db.String(255))


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)
