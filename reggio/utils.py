# coding: utf-8
from flask import flash
from flask_login import current_user


def defineMenu():
    if current_user.is_authenticated:
        menu = [(u"Главная", "main")]
        if current_user.userType == 'admin':
            menu.extend([
                (u"Пользователи", "users"),
                (u"Уроки", {u"Индивидуалки": "adminIndividualClasses"})
            ])
        elif current_user.userType == 'superAdmin':
            menu.extend([
                (u"Пользователи", "users"),
                (u"Дети", "children"),
                (u"Учителя", {u"Список": "teachers", u"Индивидуалки": "teachersIndividualClasses"}),
                (u"Уроки", {u"Индивидуалки": "adminIndividualClasses"}),
                (u"Батьки", {u"Список": "parent"}),
                ("resetDB", "resetDB")
            ])
        elif current_user.userType == 'teacher':
            menu.extend([
                (u"Учителя", {u"Индивидуалки": "teachersIndividualClasses"}),
            ])
        elif current_user.userType == 'parent':
            menu.append((u"Батьки", {u"Список": "parent"}))
        else:
            pass
        menu.append((u'Профиль', 'profile'))
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
