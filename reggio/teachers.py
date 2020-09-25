# coding: utf-8
from flask import render_template, url_for, redirect, request
from datetime import date

from reggio import app, db
from reggio.models import Teacher, Child, individualClass
from reggio.utils import *
from reggio.forms import CreateTeacherIndividual


def getChildren():
    children = Child.query.all()
    choices = [];
    for child in children:
        name = "%s %s" % (child.surname, child.name)
        choices.append((child.username, name))
    return choices

def createIndividual(username, formChild):
    childName = formChild.surname+' '+formChild.name
    newIndividual = individualClass(
        studentUsername=username,
        studentName=childName,
        timeSpent=request.form.get('timeSpent'),
        lessonDate=request.form.get('lessonDate'),
        grade=request.form.get('grade'),
        topic=request.form.get('topic'),
        comment=request.form.get('comment'),
        creationDate=date.today(),
        teacherUsername=current_user.username
    )
    db.session.add(newIndividual)
    db.session.commit()

@app.route('/teachers/individualClasses', methods=('GET', 'POST'))
def teachersIndividualClasses():
    if not checkPageAvailability(['teacher']):
        return redirect(url_for('main'))
    createIndividualForm = CreateTeacherIndividual(csrf_enabled=False)
    if createIndividualForm.validate_on_submit():
        username = request.form.get('studentUsername')
        formChild = Child.query.filter_by(username=username).first()
        if formChild:
            createIndividual(username, formChild)
            return redirect(url_for('teachersIndividualClasses'))
        else:
            flash(u'Такої дитини немає у системі, будь ласка оберіть зі списку.')
    individuals = individualClass.query.all()
    individuals.sort(key=lambda r: r.lessonDate, reverse=True)
    return render_template('teachersIndividualClasses.html',
        title='Individual',
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
        title='Teachers',
        menu=defineMenu(),
        teachers=teachers)