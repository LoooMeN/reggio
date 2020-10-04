# coding: utf-8
import os
from flask import flash
from flask_login import current_user
import sass
from reggio.models import Child, Teacher, Parent


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

def getParents():
    parents = Parent.query.all()
    choices = []
    for parent in parents:
        name = "%s %s" % (parent.surname, parent.name)
        choices.append((parent.username, name))
    return choices


def defineMenu():
    menu = [(u"Головна", "main", 'peopleIcon')]
    if current_user.userType == 'admin':
        menu.extend([
            (u"Користувачі", "users", 'peopleIcon'),
            (u"Уроки", {u"Индивидуалки": "adminIndividualClasses"}, 'peopleIcon')
        ])
    elif current_user.userType == 'superAdmin':
        menu.extend([
            (u"Користувачі", "users", 'peopleIcon'),
            (u"Учні", "children", 'peopleIcon'),
            (u"Вчителі", {u"Список": "teachers", u"Индивидуалки": "teachersIndividualClasses"}, 'peopleIcon'),
            (u"Уроки", {u"Индивидуалки": "adminIndividualClasses", }, 'peopleIcon'),
            (u"Батьки", {u"Список": "parent"}, 'peopleIcon'),
            (u"Налаштування", {u"Кольори": "color"}, 'peopleIcon'),
            ("resetDB", "resetDB", 'peopleIcon')
        ])
    elif current_user.userType == 'teacher':
        menu.extend([
            (u"Вчителі", {u"Индивидуалки": "teachersIndividualClasses"}, 'peopleIcon'),
        ])
    elif current_user.userType == 'parent':
        menu.append((u"Батьки", {u"Список": "parent"}, 'peopleIcon'))
    else:
        pass
    return menu

def checkPageAvailability(accesGranted):
    if current_user.is_authenticated:
        guestType = current_user.userType
        if guestType == 'superAdmin' or guestType in accesGranted:
            return True
    flash('Немає прав')
    return False
