# coding: utf-8
from flask import render_template, url_for, redirect

from reggio import app, db
from reggio.models import individualClass
from reggio.utils import *


def hasIndividual(userType):
    has = ["child", "teacher", "admin", "superAdmin", "tutor"]
    if userType in has:
        return True
    else:
        return False


app.jinja_env.globals.update(hasIndividual=hasIndividual)
app.jinja_env.globals.update(list=list)


@app.route('/profile/')
def profile():
    if current_user.is_authenticated:
        if hasIndividual(current_user.userType):
            if current_user.userType == "child":
                individuals = individualClass.query.filter_by(studentUsername=current_user.username).limit(20)
            else:
                individuals = individualClass.query.filter_by(teacherUsername=current_user.username).limit(20)
            return render_template(
                'profile.html',
                user=current_user,
                individuals=individuals,
                title='profile',
                menu=defineMenu())
        return render_template(
            'profile.html',
            user=current_user,
            title='profile',
            menu=defineMenu())
    return render_template(
        'main.html',
        title='Main',
        menu=defineMenu())
