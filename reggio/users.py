# coding: utf-8
import os
from flask import render_template, url_for, request, flash, redirect
from werkzeug.security import generate_password_hash

from reggio import app, db
from reggio.models import User, Child, Teacher, Parent
from reggio.forms import CreateUser
from reggio.utils import *


def deleteSubTable(user):
    entity = ''
    if user.userType == 'child':
        entity = Child.query.filter_by(username=user.username).first()
    if user.userType == 'teacher':
        entity = Teacher.query.filter_by(username=user.username).first()
    if user.userType == 'parent':
        entity = Parent.query.filter_by(username=user.username).first()

    if entity != '':
        db.session.delete(entity)


def addSubTable(user):
    entity = ''
    if user.userType == 'child':
        entity = Child()
    if user.userType == 'teacher':
        entity = Teacher()
    if user.userType == 'parent':
        entity = Parent()

    if entity != '':
        entity.username = user.username
        entity.password = user.password
        entity.avatar = user.avatar
        entity.name = user.name
        entity.surname = user.surname
        db.session.add(entity)


def updateSubtables(prevType, user):
    entity = ''
    if prevType == 'child':
        entity = Child.query.filter_by(username=user.username).first()
    elif prevType == 'teacher':
        entity = Teacher.query.filter_by(username=user.username).first()
    elif prevType == 'parent':
        entity = Parent.query.filter_by(username=user.username).first()
    else:
        addSubTable(user)

    if entity != '':
        if prevType == request.args.get("userType"):
            entity.name = request.args.get('name')
            entity.surname = request.args.get('surname')
        elif prevType != request.args.get("userType"):
            db.session.delete(entity)
            addSubTable(user)


@app.route('/updateUser')
def updateUser():
    if not checkPageAvailability([]):
        return redirect(url_for('main'))
    userID = request.args.get('id')
    user = User.query.filter_by(id=userID).first()
    user.name = request.args.get('name')
    if request.args.get('viber') != 'None':
        user.viber = request.args.get('viber')
    user.surname = request.args.get('surname')
    user.phone = request.args.get('phone')
    user.password = request.args.get('password')
    print(request.args.get('password'))
    user.email = request.args.get('email')
    user.userType = request.args.get('userType')
    prevType = request.args.get('prevType')
    updateSubtables(prevType, user)
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
            flash('Користувач відсутній')
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
