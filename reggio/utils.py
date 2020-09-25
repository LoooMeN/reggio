# coding: utf-8
from flask import flash
from flask_login import current_user


def defineMenu():
    if current_user.is_authenticated:
        if current_user.userType == 'admin':
            menu = [
                (u"Главная", "main"),
                (u"Пользователи", "users"),
                (u"Уроки", {u"Индивидуалки": "adminIndividualClasses"})
            ]
        elif current_user.userType == 'superAdmin':
            menu = [
                (u"Главная", "main"),
                (u"Пользователи", "users"),
                (u"Дети", "children"),
                (u"Учителя", {u"Список": "teachers", u"Индивидуалки": "teachersIndividualClasses"}),
                (u"Уроки", {u"Индивидуалки": "adminIndividualClasses"}),
                ("resetDB", "resetDB")
            ]
        elif current_user.userType == 'teacher':
            menu = [
                (u"Учителя", {u"Индивидуалки": "individualClasses"}),
            ]
        else :
            menu = [
                (u"Главная", "main")
            ]
        menu.append((u'Выйти', 'logout'))
    else:
        menu = [
            (u"Главная", "main"),
            (u'Войти', 'login')
        ]
    return menu

def checkPageAvailability(accesGranted):
    if current_user.is_authenticated:
        guestType = current_user.userType
        if guestType == 'superAdmin' or guestType in accesGranted:
            return True
    flash('No permission')
    return False