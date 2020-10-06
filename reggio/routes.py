# coding: utf-8
import os
from random import randrange
from datetime import datetime, timedelta

from flask import render_template, url_for, request, flash, redirect
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import current_user, login_user, logout_user
from werkzeug.utils import secure_filename

from reggio import app, db
from reggio.models import User, Child, Teacher, IndividualClass
from reggio.forms import SignInForm, CreateUser
from reggio.utils import *
import reggio.settings
import reggio.users
import reggio.children
import reggio.teachers
import reggio.admin
import reggio.profile
import reggio.parent


def compileSCSS():
    folderSCSS = os.path.join(app.root_path, 'static', 'scss')
    folderCSS = os.path.join(app.root_path, 'static', 'css')
    sass.compile(dirname=(folderSCSS, folderCSS),
                 output_style='compressed')
    return "stylesCompiled"


app.jinja_env.globals.update(compileSCSS=compileSCSS)


@app.route('/test')
def test():
    return render_template(
        'main.html',
        title='Секас',
        menu=defineMenu(),
        scss=compileSCSS()
    )


@app.route('/')
def main():
    if current_user.is_authenticated:
        return render_template('dashboard.html', title='Головна', menu=defineMenu())
    return redirect(url_for('login'))


@app.route('/login', methods=('GET', 'POST'))
def login():
    signinForm = SignInForm(crsf_enabled=False)
    if signinForm.validate_on_submit():
        user = User.query.filter_by(username=request.form.get('username')).first()
        if user and check_password_hash(user.password, request.form.get('password')):
            login_user(user)
            return redirect(url_for('main'))
        else:
            flash('Невірні дані')
    elif current_user.is_authenticated:
        return redirect(url_for('main'))
    return render_template(
        'login.html',
        signinForm=signinForm)


@app.route('/logout')
def logout():
    if current_user.is_authenticated:
        logout_user()
    return redirect(url_for('login'))


@app.route('/resetdb')
def resetDB():
    db.drop_all()
    db.create_all()
    admin = User(username='admin', email='looomen@hotmail.com', userType='superAdmin', name='Кіт',
                 surname='Василь', password=generate_password_hash('123'),
                 avatar=os.path.join('static', 'images', 'avatars', 'defaultUserImage.png'))
    db.session.add(admin)

    children = []
    users = []
    teachers = []
    individuals = []
    counter = 1
    while counter < 16:
        username = 'child' + str(counter)
        email = 'child' + str(counter) + '@gmail.com'
        userType = 'child'
        name = 'child' + str(counter)
        surname = 'childovich' + str(counter)
        password = generate_password_hash('123')
        avatar = os.path.join('static', 'images', 'avatars', 'defaultUserImage.png')
        users.append(User(
            username=username,
            userType=userType,
            email=email,
            name=name,
            surname=surname,
            password=password,
            avatar=avatar
        ))
        children.append(Child(
            username=username,
            name=name,
            surname=surname,
            avatar=avatar
        ))
        counter += 1

    counter = 1
    while counter < 16:
        username = 'teacher' + str(counter)
        email = 'teacher' + str(counter) + '@gmail.com'
        userType = 'teacher'
        name = 'teacher' + str(counter)
        surname = 'teacherovich' + str(counter)
        password = generate_password_hash('123')
        avatar = os.path.join('static', 'images', 'avatars', 'defaultUserImage.png')
        users.append(User(
            username=username,
            userType=userType,
            name=name,
            email=email,
            surname=surname,
            password=password,
            avatar=avatar
        ))
        teachers.append(Teacher(
            username=username,
            name=name,
            surname=surname,
            avatar=avatar
        ))
        counter += 1

    for childItem in children:
        teacher = teachers[randrange(5)]
        teacherUsername = teacher.username
        teacherName = teacher.surname + ' ' + teacher.name
        studentUsername = childItem.username
        studentName = childItem.surname + ' ' + childItem.name
        timeSpent = randrange(15, 45)
        creationDate = str(randrange(2010, 2021)) + '-' + str(randrange(1, 13)) + '-' + str(
            randrange(1, 28)) + ' 00:00:0'
        lessonDate = str(randrange(2010, 2021)) + '-' + str(randrange(1, 13)) + '-' + str(randrange(1, 28)) + ' 00:00:0'
        grade = randrange(12)
        topic = 'flexi'
        individuals.append(IndividualClass(
            teacherUsername=teacherUsername,
            teacherName=teacherName,
            studentUsername=studentUsername,
            studentName=studentName,
            timeSpent=timeSpent,
            creationDate=creationDate,
            lessonDate=lessonDate,
            grade=grade,
            topic=topic
        ))
        db.session.add(childItem)

    for teacherItem in teachers:
        db.session.add(teacherItem)

    for individualItem in individuals:
        db.session.add(individualItem)

    for userItem in users:
        db.session.add(userItem)

    db.session.commit()
    return redirect(url_for('main'))
