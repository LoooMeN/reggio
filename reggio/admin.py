# coding: utf-8
import os
from re import I
import time
import pathlib
from datetime import datetime
from os.path import dirname, abspath

from flask import request, flash, redirect, url_for, render_template, send_file
from sqlalchemy import and_
from reggio import app, db
from reggio.models import IndividualClass, Teacher
from reggio.forms import CreateTeacherIndividual as form
from reggio.utils import *

from reggio.forms import GetIndividual
import pandas as pd

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
    error = request.args.get('error')
    if (error == "1"):
        flash("Не обрано поле")
    cleanTemp()
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
    IndividualClassesIDs = request.args.get('ids')
    if (IndividualClassesIDs):
        IndividualClassesIDs = IndividualClassesIDs.split(';')
        for IndividualClassID in IndividualClassesIDs:
            selectedToDel = IndividualClass.query.filter_by(id=IndividualClassID).first()
            db.session.delete(selectedToDel)
        db.session.commit()
        if (request.args.get('reload')):
            return redirect(url_for('adminIndividualClasses'))
        return "0"
    return "1"


def createXLSX(IndividualClassesIDs):
    table = {"Створено": [],
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
        table["Створено"].append(selectedToDownload.creationDate)
        table["Вчитель"].append(selectedToDownload.teacherName)
        table["Учень"].append(selectedToDownload.studentName)
        table["Часу витрачено"].append(selectedToDownload.timeSpent)
        table["Оцінка"].append(selectedToDownload.grade)
        table["Тема"].append(selectedToDownload.topic)
        table["Коментар"].append(selectedToDownload.comment)
        table["Дата уроку"].append(selectedToDownload.lessonDate)
    return table

def cleanTemp():
    tempDirPath = os.path.join(app.root_path, 'static', 'temp')
    tempFiles = os.listdir(tempDirPath)
    for file in tempFiles:
        file = os.path.join(app.root_path, 'static', 'temp', file)
        os.remove(file)
        return 1


@app.route('/admin/downloadXLSX', methods=["GET"])
def downloadXLSX():
    filename = os.path.join(app.root_path, 'static', 'temp', request.args.get('filename'))
    return send_file(filename, as_attachment=True, attachment_filename=request.args.get('filename'))


@app.route('/admin/createIndividualClassXLSX', methods=["GET"])
def createIndividualClassXLSX():
    IndividualClassesIDs = request.args.get('ids').split(";")
    PreferredFilename = request.args.get('prefferedFilename')

    if not PreferredFilename:
        PreferredFilename = "individual.xlsx"
    else:
        PreferredFilename += ".xlsx"

    if (IndividualClassesIDs[0]):
        df1 = pd.DataFrame(createXLSX(IndividualClassesIDs))
        filepath = os.path.join(app.root_path, 'static', 'temp', PreferredFilename)
        df1.to_excel(filepath, sheet_name='Individual')
        return PreferredFilename
    return "1"