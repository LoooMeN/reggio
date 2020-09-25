# coding: utf-8
import os
from flask import render_template, url_for, request, flash, redirect
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import current_user, login_user, logout_user
from werkzeug.utils import secure_filename

from reggio import app, db
from reggio.models import User, Child, Teacher, individualClass
from reggio.forms import SignInForm, CreateUser
from reggio.utils import *
import reggio.users
import reggio.children
import reggio.teachers


@app.route('/test')
def test():
    return 'sex'

@app.route('/admin/individualClasses')
def adminIndividualClasses():
    if not checkPageAvailability(['admin']):
        return redirect(url_for('main'))
    individualClasses = individualClass.query.all()
    return render_template(
        'adminIndividualClasses.html',
        individualClasses=individualClasses,
        title=u'Індивідулки',
        menu=defineMenu())

@app.route('/') # dashboard if admin else logo prompt
def main():
    if current_user.is_authenticated:
        return render_template('child.html', user=current_user.username.upper(), title='Main', menu=defineMenu())
    return render_template(
        'tsar.html',
        title='Main',
        menu=defineMenu())

@app.route('/login', methods=('GET', 'POST'))
def login():
    signinForm = SignInForm(csrf_enabled=False)
    if signinForm.validate_on_submit():
        user = User.query.filter_by(username=request.form.get('username')).first()
        if user and check_password_hash(user.password, request.form.get('password')):
            login_user(user)
            return redirect(url_for('main'))
        else:
            flash('Incorrect credentials, homie')
    elif current_user.is_authenticated:
        return redirect(url_for('main'))
    return render_template(
        'login.html',
        signinForm=signinForm,
        title='Login',
        menu=defineMenu())

@app.route('/logout')
def logout():
    if current_user.is_authenticated:
        logout_user()
    return redirect(url_for('main'))

@app.route('/resetdb')
def resetDB():
    db.drop_all()
    db.create_all()
    admin = User(username='admin', email='looomen@hotmail.com', userType='superAdmin', password=generate_password_hash('123'), avatar=os.path.join('static', 'images', 'avatars', 'defaultUserImage.png'))
    db.session.add(admin)
    db.session.commit()
    return redirect(url_for('main'))