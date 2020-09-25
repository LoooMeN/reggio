# coding: utf-8
from flask import render_template, url_for, redirect

from reggio import app, db
from reggio.models import Child
from reggio.utils import *

@app.route('/profile/')
def profile():
    if current_user.is_authenticated:
        return render_template('profile.html', user=current_user, title='profile', menu=defineMenu())
    return render_template(
        'main.html',
        title='Main',
        menu=defineMenu())