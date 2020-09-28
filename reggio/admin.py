# coding: utf-8
import os
import pathlib
from datetime import datetime

from flask import request, flash, redirect, url_for, render_template
from sqlalchemy import and_
from reggio import app, db
from reggio.models import IndividualClass, Teacher
from reggio.forms import CreateTeacherIndividual as form
from reggio.utils import *

from reggio.forms import GetIndividual
import pandas as pd
import xlsxwriter

from datetime import datetime, timedelta


def filterIndividuals():
    if request.form.get('timeBefore') and request.form.get('timeAfter'):
        before = datetime.strptime(request.form.get('timeBefore') + ' 00:00:00', '%Y-%m-%d %H:%M:%S')
        after = datetime.strptime(request.form.get('timeAfter') + ' 00:00:00', '%Y-%m-%d %H:%M:%S')
        if before > after:
            return None
    individualClasses = IndividualClass.query.all()
    if request.form.get('studentUsername'):
        individualClasses = [n for n in individualClasses if n.studentUsername == request.form.get('studentUsername')]
    if request.form.get('teacherUsername'):
        individualClasses = [n for n in individualClasses if n.teacherUsername == request.form.get('teacherUsername')]
    if request.form.get('timeBefore'):
        individualClasses = [n for n in individualClasses if
                             n.creationDate <= datetime.strptime(request.form.get('timeBefore') + ' 00:00:00',
                                                                 '%Y-%m-%d %H:%M:%S')]
    if request.form.get('timeAfter'):
        individualClasses = [n for n in individualClasses if
                             n.creationDate >= datetime.strptime(request.form.get('timeAfter') + ' 00:00:00',
                                                                 '%Y-%m-%d %H:%M:%S')]
    return individualClasses


@app.route('/admin/individualClasses', methods=('GET', 'POST'))
def adminIndividualClasses():
    if not checkPageAvailability(['admin']):
        return redirect(url_for('main'))
    GetIndividualForm = GetIndividual()
    if GetIndividualForm.validate_on_submit():
        individualClasses = filterIndividuals()
        if individualClasses is None:
            return redirect(url_for('adminIndividualClasses'))
    else:
        individualClasses = IndividualClass.query.all()
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
    IndividualClasses = IndividualClass.query.filter_by(id=IndividualClassesID).first()
    db.session.delete(IndividualClasses)
    db.session.commit()
    return redirect(url_for('adminIndividualClasses'))


@app.route('/admin/deleteIndividualClasses', methods=["GET"])
def deleteIndividualClasses():
    if not checkPageAvailability(['admin']):
        return redirect(url_for('main'))
    IndividualClassesIDs = request.args.get('ids')
    IndividualClassesIDs = IndividualClassesIDs.split(';')
    for IndividualClassID in IndividualClassesIDs:
        selectedToDel = IndividualClass.query.filter_by(id=IndividualClassID).first()
        db.session.delete(selectedToDel)
    db.session.commit()
    return redirect(url_for('adminIndividualClasses'))


@app.route('/admin/downloadIndividualClasses', methods=["GET"])
def downloadIndividualClasses():
    if not checkPageAvailability(['admin']):
        return redirect(url_for('main'))
    IndividualClassesIDs = request.args.get('ids')
    IndividualClassesIDs = IndividualClassesIDs.split(';')
    data = {"Створено": [],
            "Вчитель": [],
            "Учень": [],
            "Часу витрачено": [],
            "Оцінка": [],
            "Тема": [],
            "Коментар": [],
            "Дата уроку": []
            }
    for IndividualClassID in IndividualClassesIDs:
        selectedToDownload = IndividualClass.query.filter_by(id=IndividualClassID).first()
        data["Створено"].append(selectedToDownload.creationDate)
        data["Вчитель"].append(selectedToDownload.teacherName)
        data["Учень"].append(selectedToDownload.studentName)
        data["Часу витрачено"].append(selectedToDownload.timeSpent)
        data["Оцінка"].append(selectedToDownload.grade)
        data["Тема"].append(selectedToDownload.topic)
        data["Коментар"].append(selectedToDownload.comment)
        data["Дата уроку"].append(selectedToDownload.lessonDate)
    DataFrame = pd.DataFrame(data)
    # ПОФИКСИТЬ ПАТЧ
    writer = pd.ExcelWriter('individualki.xlsx', engine='xlsxwriter')
    DataFrame.to_excel(writer, sheet_name='Individual')
    writer.save()
    return redirect(url_for('adminIndividualClasses'))
