# coding: utf-8
from flask import render_template, url_for, request, flash, redirect

from reggio import app, db
from reggio.models import Parent, Child
from reggio.users import updateSubtables
from reggio.utils import *


def updateParent():
    parents = Parent.query.all()
    for parent in parents:
        if parent.children != '' and parent.children is not None:
            childrenList = parent.children.split(';')
            for childUsername in childrenList:
                userChild = Child.query.filter_by(username=childUsername).first()
                if userChild is not None and userChild != '':
                    childParents = userChild.parents.split(';')
                    if parent.username in childParents:
                        pass
                    else:
                        childrenList.remove(childUsername)
                else:
                    childrenList.remove(childUsername)
            parent.children = ';'.join(childrenList)
    db.session.commit()


@app.route('/parent/')
def parent():
    if not checkPageAvailability(["parent"]):
        return redirect(url_for('main'))
    updateParent()
    parents = Parent.query.all()
    return render_template('parent.html',
                           title=u'Батьки',
                           menu=defineMenu(),
                           parents=parents)
