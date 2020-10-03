# coding: utf-8
from flask import render_template, url_for, redirect, request

from reggio import app, db
from reggio.models import Child, User, Parent
from reggio.users import updateSubtables
from reggio.utils import *


def convertParents(name_username, to):
    if to == "name":
        if name_username is None:
            return ''
        parents = name_username.split(';')
        parentsName = []
        for parent in parents:
            parentUsr = Parent.query.filter_by(username=parent).first()
            if parentUsr is not None:
                parentName = parentUsr.surname + " " + parentUsr.name
                parentsName.append(parentName)
        parentsName = ';'.join(parentsName)
        return parentsName
    else:
        parentName = name_username.split(';')
        parentsUsername = []
        parents = Parent.query.all()
        for parent in parents:
            if parent.surname + " " + parent.name in parentName:
                parentsUsername.append(parent.username)
        parentsUsername = ';'.join(parentsUsername)
        return parentsUsername


app.jinja_env.globals.update(convertParents=convertParents)


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
    user = Child.query.filter_by(id=userID).first()
    print(request.args.get('parents'))
    convert = convertParents(request.args.get('parents'), "username")
    parents = validateParent(convert)
    user.parents = ';'.join(parents)
    for parent in parents:
        parent = Parent.query.filter_by(username=parent).first()
        if parent.children is None:
            parent.children = user.username
        else:
            children = parent.children.split(';')
            if user.username not in children:
                parent.children += ';' + user.username
    try:
        db.session.commit()
    except:
        flash(u'Помилка запису в базу данних. Можливо ви ввели вже існуючий юзернейм чи пошту.')
    return redirect(url_for('children'))
