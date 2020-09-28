# coding: utf-8
from flask import render_template, url_for, request, flash, redirect
from datetime import datetime, timedelta

from reggio import app, db
from reggio.models import IndividualClass, User, Teacher, Child
from reggio.users import updateSubtables
from reggio.utils import *


def hasIndividual(userType):
    legitimateUsersForIndividuals = ["child", "teacher", "admin", "superAdmin", "tutor"]
    if userType in legitimateUsersForIndividuals:
        return True
    else:
        return False


@app.route('/profile/')
def profile():
    if not current_user.is_authenticated:
        return redirect(url_for('main'))
    if hasIndividual(current_user.userType):
        if current_user.userType == "child":
            individuals = IndividualClass.query.filter_by(studentUsername=current_user.username).filter(
                IndividualClass.creationDate > datetime.today() - timedelta(days=14))
        else:
            individuals = IndividualClass.query.filter_by(teacherUsername=current_user.username).filter(
                IndividualClass.creationDate > datetime.today() - timedelta(days=14))
        return render_template(
            'profile.html',
            user=current_user,
            individuals=individuals,
            title='Профіль',
            menu=defineMenu())
    return render_template(
        'profile.html',
        user=current_user,
        title='Профіль',
        menu=defineMenu())


@app.route('/profile/change')
def updateProfile():
    if not current_user.is_authenticated:
        return redirect(url_for('main'))
    user = User.query.filter_by(id=current_user.id).first()
    user.name = request.args.get('name')
    user.viber = request.args.get('viber')
    user.surname = request.args.get('surname')
    user.phone = request.args.get('phone')
    user.email = request.args.get('email')
    prevType = request.args.get('prevType')
    updateSubtables(prevType, user)
    try:
        db.session.commit()
    except:
        flash(u'Помилка запису в базу данних. Можливо ви ввели вже існуючий юзернейм чи пошту..')
    return redirect(url_for('profile'))
