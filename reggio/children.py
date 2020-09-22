# coding: utf-8
from flask import render_template, url_for, redirect

from reggio import app, db
from reggio.models import Child
from reggio.utils import *


@app.route('/children')
def children():
    if not checkPageAvailability([]):
        return redirect(url_for('main'))
    children = Child.query.all()
    return render_template('children.html',
        title='Children',
        menu=defineMenu(),
        children=children)