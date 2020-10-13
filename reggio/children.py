# coding: utf-8
from flask import render_template, url_for, redirect, request

from reggio import app, db
from reggio.models import Child, User, Parent
from reggio.users import updateSubtables
from reggio.utils import *


def validateParent(parentList):
    parentList = parentList.split(';')
    validList = []
    for parent in parentList:
        if Parent.query.filter_by(username=parent).first() is not None:
            validList.append(parent)
    validList = list(dict.fromkeys(validList))
    return validList


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
    child = Child.query.filter_by(id=userID).first()
    parentsUsername = convertUsername(request.args.get('parents'), 'username')
    parents = validateParent(parentsUsername)
    child.parents = ';'.join(parents)
    for parent in parents:
        parent = Parent.query.filter_by(username=parent).first()
        if parent.children is None:
            parent.children = child.username
        else:
            children = parent.children.split(';')
            if child.username not in children:
                parent.children += ';' + child.username
    try:
        db.session.commit()
    except:
        flash(u'Помилка запису в базу данних. Можливо ви ввели вже існуючий юзернейм чи пошту.')
    return redirect(url_for('children'))
