# coding: utf-8
from flask import flash
from flask_login import current_user

from reggio.models import Child, Teacher

def getChildren():
    children = Child.query.all()
    choices = []
    for child in children:
        name = "%s %s" % (child.surname, child.name)
        choices.append((child.username, name))
    return choices

def getTeachers():
    teachers = Teacher.query.all()
    choices = []
    for teacher in teachers:
        name = "%s %s" % (teacher.surname, teacher.name)
        choices.append((teacher.username, name))
    return choices

def defineMenu():
    if current_user.is_authenticated:
        menu = [(u"Головна", "main")]
        if current_user.userType == 'admin':
            menu.extend([
                (u"Користувачі", "users"),
                (u"Уроки", {u"Индивидуалки": "adminIndividualClasses"})
            ])
        elif current_user.userType == 'superAdmin':
            menu.extend([
                (u"Користувачі", "users"),
                (u"Учні", "children"),
                (u"Вчителі", {u"Список": "teachers", u"Индивидуалки": "teachersIndividualClasses"}),
                (u"Уроки", {u"Индивидуалки": "adminIndividualClasses"}),
                (u"Батьки", {u"Список": "parent"}),
                ("resetDB", "resetDB")
            ])
        elif current_user.userType == 'teacher':
            menu.extend([
                (u"Вчителі", {u"Индивидуалки": "teachersIndividualClasses"}),
            ])
        elif current_user.userType == 'parent':
            menu.append((u"Батьки", {u"Список": "parent"}))
        else:
            pass
        menu.append((u'Профіль', 'profile'))
        menu.append((u'Вийти', 'logout'))
    else:
        menu = [
            (u'Авторизація', 'login')
        ]
    return menu


def checkPageAvailability(accesGranted):
    if current_user.is_authenticated:
        guestType = current_user.userType
        if guestType == 'superAdmin' or guestType in accesGranted:
            return True
    flash('Немає прав')
    return False
