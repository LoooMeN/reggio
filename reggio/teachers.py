# coding: utf-8
from flask import render_template, url_for, redirect, request
from datetime import date, datetime, timedelta

from reggio import app, db
from reggio.models import Teacher, Child, IndividualClass
from reggio.utils import *
from reggio.forms import CreateTeacherIndividual


def createIndividual(username, formChild):
    childName = formChild.surname + ' ' + formChild.name
    teacherName = current_user.surname + ' ' + current_user.name
    newIndividual = IndividualClass(
        teacherUsername=current_user.username,
        teacherName=teacherName,
        studentUsername=username,
        studentName=childName,
        timeSpent=request.form.get('timeSpent'),
        lessonDate=request.form.get('lessonDate'),
        grade=request.form.get('grade'),
        topic=request.form.get('topic'),
        comment=request.form.get('comment'),
        creationDate=date.today()
    )
    db.session.add(newIndividual)
    db.session.commit()


@app.route('/teachers/individualClasses', methods=('GET', 'POST'))
def teachersIndividualClasses():
    if not checkPageAvailability(['teacher']):
        return redirect(url_for('main'))
    createIndividualForm = CreateTeacherIndividual()
    if createIndividualForm.validate_on_submit():
        username = request.form.get('studentUsername')
        formChild = Child.query.filter_by(username=username).first()
        if formChild:
            createIndividual(username, formChild)
        else:
            flash(u'Такої дитини немає у системі, будь ласка оберіть зі списку.')
        return redirect(url_for('teachersIndividualClasses'))
    individuals = IndividualClass.query.filter_by(teacherUsername=current_user.username).filter(
        IndividualClass.creationDate > datetime.today() - timedelta(days=14)).all()
    if individuals is None:
        individuals = False
    print(individuals)
    return render_template('teachersIndividualClasses.html',
                           title='Індивідуалки',
                           menu=defineMenu(),
                           form=createIndividualForm,
                           children=getChildren(),
                           individuals=individuals)


@app.route('/teachers')
def teachers():
    if not checkPageAvailability([]):
        return redirect(url_for('main'))
    teachers = Teacher.query.all()
    return render_template('teachers.html',
                           title='Вчителі',
                           menu=defineMenu(),
                           teachers=teachers)
