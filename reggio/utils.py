# coding: utf-8
import os
from flask import flash
from flask_login import current_user
from reggio import app
from reggio.models import Child, Teacher, Parent, User
import sass


def replaceListItem(array, frm, to):
    if array and frm and to:
        for index, value in enumerate(array):
            if value == frm:
                array[index] = to
    return array


def convertUsername(frm, to):
    if frm is not None and frm != '':
        List = frm.split(';')
        if to == "name":
            for frm in List:
                user = User.query.filter_by(username=frm).first()
                if user is not None:
                    fullName = user.surname + " " + user.name
                    List = replaceListItem(List, frm, fullName)
                else:
                    List.remove(frm)
        if to == "username":
            users = User.query.all()
            for item in List:
                item.replace('&nbsp;', '')
            for user in users:
                fullName = user.surname + " " + user.name
                if fullName in List:
                    List = replaceListItem(List, fullName, user.username)
            for x in List:
                if " " in x:
                    List.remove(x)
        if len(List) > 1:
            return ';'.join(List)
        else:
            return List[0]
    return "None"


app.jinja_env.globals.update(convertUsername=convertUsername)


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
            (u"Адмін", {u"Індивідуалки": "adminIndividualClasses", u"Групи": "childrenGroups", u"Користувачі": "users"}, 'peopleIcon'),
        ])
    elif current_user.userType == 'superAdmin':
        menu.extend([
            (u"Учні", "children", 'peopleIcon'),
            (u"Вчителі", {u"Список": "teachers", u"Індивідуалки": "teachersIndividualClasses"}, 'peopleIcon'),
            (u"Адмін", {u"Індивідуалки": "adminIndividualClasses", u"Групи": "childrenGroups", u"Користувачі": "users", "resetDB": "resetDB"}, 'peopleIcon'),
            (u"Батьки", {u"Список": "parent"}, 'peopleIcon'),
            # (u"Налаштування", {u"Кольори": "color"}, 'peopleIcon'),
        ])
    elif current_user.userType == 'teacher':
        menu.extend([
            (u"Вчителі", {u"Індивідуалки": "teachersIndividualClasses"}, 'peopleIcon'),
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
