# coding: utf-8
from datetime import datetime

from flask import request, flash, redirect, url_for, render_template
from sqlalchemy import and_
from reggio import app, db
from reggio.models import individualClass, Teacher
from reggio.utils import *

from reggio.forms import GetIndividual

from datetime import datetime, timedelta

def filterIndividuals():

    individualClasses = individualClass.query.all()
    if request.form.get('studentUsername'):
        individualClasses = [n for n in individualClasses if n.studentUsername == request.form.get('studentUsername')]
    if request.form.get('teacherUsername'):
        individualClasses = [n for n in individualClasses if n.teacherUsername == request.form.get('teacherUsername')]
    if request.form.get('timeBefore'):
        individualClasses = [n for n in individualClasses if n.creationDate <= datetime.strptime(request.form.get('timeBefore'), '%y-%m-%d').date()]
    if request.form.get('timeAfter'):
        individualClasses = [n for n in individualClasses if n.creationDate >= datetime.strptime(request.form.get('timeAfter'), '%y-%m-%d').date()]
    return individualClasses


@app.route('/admin/individualClasses', methods=('GET', 'POST'))
def adminIndividualClasses():
    if not checkPageAvailability(['admin']):
        return redirect(url_for('main'))
    GetIndividualForm = GetIndividual(csrf_enabled=False)
    if GetIndividualForm.validate_on_submit():
<<<<<<< HEAD
        individualClasses = filterIndividuals()
=======
>>>>>>> 19253adac94a77c86caa5e77f4e3737ae5943ce7
        flash(request.form)
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


@app.route('/admin/deleteIndividualClass', methods=["GET"])
def deleteIndividualClass():
    if not checkPageAvailability(['admin']):
        return redirect(url_for('main'))
    IndividualClassesID = request.args.get('id')
    IndividualClasses = individualClass.query.filter_by(id=IndividualClassesID).first()
    db.session.delete(IndividualClasses)
    db.session.commit()
    return redirect(url_for('adminIndividualClasses'))

@app.route('/admin/deleteIndividualClasses', methods=["GET"])
def deleteIndividualClasses():
    if not checkPageAvailability(['admin']):
        return redirect(url_for('main'))
    IndividualClassesIDs = request.args.get('ids')
    IndividualClassesIDs = IndividualClassesIDs.split(';')
    for IndividualClass in IndividualClassesIDs:
        selectedToDel = individualClass.query.filter_by(id=IndividualClass).first()
        db.session.delete(selectedToDel)
    db.session.commit()
    return 'deleted'