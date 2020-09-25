# coding: utf-8
from flask import render_template, url_for, redirect

from reggio import app, db
from reggio.models import individualClass
from reggio.utils import *

@app.route('/profile/')
def profile():
    if current_user.is_authenticated:
        if current_user.userType == "child":
            individuals = individualClass.query.filter_by(studentUsername=current_user.username)
            return render_template('profile.html', user=current_user, individuals=individuals, title='profile', menu=defineMenu())
        return render_template('profile.html', user=current_user, title='profile', menu=defineMenu())
    return render_template(
        'main.html',
        title='Main',
        menu=defineMenu())