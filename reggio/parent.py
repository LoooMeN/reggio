# coding: utf-8
from flask import render_template, url_for, request, flash, redirect


from reggio import app, db
from reggio.models import Parent
from reggio.users import updateSubtables
from reggio.utils import *

@app.route('/parent/')
def parent():
    if not checkPageAvailability(["parent"]):
        return redirect(url_for('main'))
    parents = Parent.query.all()
    return render_template('parent.html',
        title=u'Батьки',
        menu=defineMenu(),
        parents=parents)