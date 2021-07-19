# coding: utf-8
import os
from flask import render_template, url_for, request, flash, redirect
from werkzeug.security import generate_password_hash

from reggio import app, db
from reggio.models import User, Child, Teacher, Parent
from reggio.forms import CreateUser
from reggio.utils import *


def deleteSubTable(user):
    if user.userType == 'child':
        entity = Child.query.filter_by(username=user.username).first()
    if user.userType == 'teacher':
        entity = Teacher.query.filter_by(username=user.username).first()
    if user.userType == 'parent':
        entity = Parent.query.filter_by(username=user.username).first()

    if entity:
        db.session.delete(entity)


def addSubTable(user):
    if user.userType == 'child':
        entity = Child()
    if user.userType == 'teacher':
        entity = Teacher()
    if user.userType == 'parent':
        entity = Parent()

    if entity:
        entity.username = user.username
        entity.avatar = user.avatar
        entity.name = user.name
        entity.surname = user.surname
        db.session.add(entity)


def updateSubtables(user, prevType=""):
    if prevType == "child" or prevType == "teacher" or prevType == "parent":
        user.userType = prevType
        deleteSubTable(user)
        if user.userType == 'child':
            entity = Child.query.filter_by(username=user.username).first()
        if user.userType == 'teacher':
            entity = Teacher.query.filter_by(username=user.username).first()
        if user.userType == 'parent':
            entity = Parent.query.filter_by(username=user.username).first()
        if entity:
            entity.name = user.name
            entity.surname = user.surname
            db.session.commit()

    if user.userType == 'child' or user.userType == 'teacher' or user.userType == 'parent':
        addSubTable(user)


@app.route('/editUser')
def editUser():
    if not checkPageAvailability([]):
        return redirect(url_for('main'))
    userID = request.args.get('id')
    user = User.query.filter_by(id=userID).first()
    if not userID or not user:
        return redirect(url_for('main'))
    return render_template('editUser.html',
                        user=user,
                        title='Редагування користувача',
                        menu=defineMenu())



@app.route('/updateUser')
def updateUser():
    if not checkPageAvailability([]):
        return redirect(url_for('main'))
    userID = request.args.get('id')
    user = User.query.filter_by(id=userID).first()
    user.name = request.args.get('name')
    if request.args.get('viber'):
        user.viber = request.args.get('viber')
    user.surname = request.args.get('surname')
    if request.args.get('phone'):
        user.phone = request.args.get('phone')
    if request.args.get('password'):
        user.password = generate_password_hash(request.args.get('password'))
    user.email = request.args.get('email')
    if request.args.get('userType'):
        user.userType = request.args.get('userType')
    if request.args.get('prevType'):
        prevType = request.args.get('prevType')
        updateSubtables(user, prevType)
    updateSubtables(user)
    try:
        db.session.commit()
    except:
        flash(u'Помилка запису в базу данних. Можливо ви ввели вже існуючий юзернейм чи пошту.')
    return redirect(url_for('users'))


@app.route('/updateProfile')
def updateUserProfile():
    if not checkPageAvailability([]):
        return redirect(url_for('main'))
    userID = request.args.get('id')
    user = User.query.filter_by(id=userID).first()
    user.name = request.args.get('name')
    if request.args.get('viber') != 'None':
        user.viber = request.args.get('viber')
    user.surname = request.args.get('surname')
    user.phone = request.args.get('phone')
    user.email = request.args.get('email')
    user.userType = user.userType
    prevType = user.userType
    updateSubtables(user, prevType)
    try:
        db.session.commit()
    except:
        flash(u'Помилка запису в базу данних. Можливо ви ввели вже існуючий юзернейм чи пошту.')
    return redirect(url_for('users'))


def addUser(addUserForm):
    avatar = os.path.join('static', 'images', 'avatars', 'defaultUserImage.png')
    if addUserForm.avatar.data:
        avatar = os.path.join('static', 'images', 'avatars', addUserForm.avatar.data.filename)
    newUser = User(
        username=request.form.get('username'),
        email=request.form.get('email'),
        userType=request.form.get('userType'),
        password=generate_password_hash(request.form.get('password')),
        name=request.form.get('name'),
        surname=request.form.get('surname'),
        phone=request.form.get('phone'),
        viber=request.form.get('viber'),
        avatar=avatar
    )
    db.session.add(newUser)
    addSubTable(newUser)
    db.session.commit()


@app.route('/users', methods=('GET', 'POST'))
def users():
    if not checkPageAvailability([]):
        return redirect(url_for('main'))
    addUserForm = CreateUser()
    if addUserForm.validate_on_submit():
        username = request.form.get('username')
        email = request.form.get('email')
        if User.query.filter_by(username=username).first() or User.query.filter_by(email=email).first():
            flash('Такий користувач вже зареєстрований')
        else:
            addUser(addUserForm)
            return redirect(url_for('users'))
    users = User.query.all()
    return render_template('users.html',
                           users=users,
                           form=addUserForm,
                           title='Користувачі',
                           menu=defineMenu())


@app.route('/deleteUser', methods=["GET"])
def deleteUser():
    if not checkPageAvailability([]):
        return redirect(url_for('main'))
    userID = request.args.get('id')
    user = User.query.filter_by(id=userID).first()
    avatarFilename = os.path.split(user.avatar)[-1]
    if avatarFilename != 'defaultUserImage.png':
        os.remove(os.path.join(app.instance_path, user.avatar))
    deleteSubTable(user)
    db.session.delete(user)
    db.session.commit()
    return redirect(url_for('users'))
