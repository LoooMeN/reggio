# coding: utf-8
from flask import render_template, url_for, redirect, request

from reggio import app, db
from reggio.models import Child, User
from reggio.users import updateSubtables
from reggio.utils import *


@app.route('/children')
def children():
    if not checkPageAvailability([]):
        return redirect(url_for('main'))
    children = Child.query.all()
    parents = getParents()
    return render_template('children.html',
                           title='Учні',
                           menu=defineMenu(),
                           children=children,
                           parents=parents)


@app.route('/bindParent')
def bindParent():
    if not checkPageAvailability([]):
        return redirect(url_for('main'))
    userID = request.args.get('id')
    user = Child.query.filter_by(id=userID).first()
    user.parents = request.args.get('parents')
    print(user.parents)
    try:
        db.session.commit()
    except:
        flash(u'Помилка запису в базу данних. Можливо ви ввели вже існуючий юзернейм чи пошту.')
    return redirect(url_for('children'))
