# coding: utf-8
from flask import request, flash, redirect, url_for, render_template

from reggio import app, db
from reggio.models import individualClass, Teacher
from reggio.utils import *


from reggio.forms import GetIndividual

@app.route('/admin/individualClasses', methods=('GET', 'POST'))
def adminIndividualClasses():
    if not checkPageAvailability(['admin']):
        return redirect(url_for('main'))
    GetIndividualForm = GetIndividual(csrf_enabled=False)
    if GetIndividualForm.validate_on_submit():
        # individualClass
        flash(request.form)
    else:
        individualClasses = individualClass.query.all()
    individualClasses.sort(key=lambda r: r.creationDate, reverse=True)
    teacherList = getTeachers()
    childrenList = getChildren()
    return render_template(
        'adminIndividualClasses.html',
        teacherList=teacherList,
        form=GetIndividualForm,
        childrenList=childrenList,
        individualClasses=individualClasses,
        title=u'Індивідулки',
        menu=defineMenu())


@app.route('/admin/deleteIndividualClasses', methods=["GET"])
def deleteIndividualClasses():
    if not checkPageAvailability(['admin']):
        return redirect(url_for('main'))
    IndividualClassesID = request.args.get('id')
    IndividualClasses = db.session.merge(individualClass.query.filter_by(id=IndividualClassesID).first())
    db.session.delete(IndividualClasses)
    db.session.commit()
    return redirect(url_for('adminIndividualClasses'))
