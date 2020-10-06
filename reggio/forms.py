# coding: utf-8
from datetime import datetime
import os

import imagesize
from flask import flash
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, IntegerField, SubmitField, TextAreaField, SelectField, DateField
from wtforms.validators import DataRequired, Email, Length, ValidationError, Optional
from flask_wtf.file import FileField, FileRequired, FileAllowed
from werkzeug.utils import secure_filename
from reggio import app
from reggio.models import Child, Teacher


def existanceValidator(entityType):
    errorMessages = {
        "teacher": u"Такого вчителя не існує.",
        "child": u"Такого учня не існує."
    }

    def _existanceValidator(form, field):
        username = field.data
        selection = ''
        if entityType == 'teacher':
            selection = Teacher.query.filter_by(username=username).first()
        else:
            selection = Child.query.filter_by(username=username).first()
        if not selection:
            raise ValidationError(errorMessages[entityType])

    return _existanceValidator


def imageSizeValidator(min=-1, max=-1, directory='static'):
    sizeMessage = u"Фото повинно бути не менше %d та не більше %d пікселів обом параметрам." % (min, max)
    nameMessage = u"Фото з таким ім'ям уже існує, перейменуйте будьласка."

    def _imageSizeValidator(form, field):
        f = field.data
        if f:
            filename = secure_filename(f.filename)
            filepath = os.path.join(
                app.root_path, directory, filename
            )
            if os.path.exists(filepath):
                raise ValidationError(nameMessage)
            f.save(filepath)
            width, height = imagesize.get(filepath)
            if width < min or width > max or height < min or height > max:
                os.remove(filepath)
                raise ValidationError(sizeMessage)

    return _imageSizeValidator


class SignInForm(FlaskForm):
    username = StringField('Юзернейм', [
        DataRequired()], render_kw={'autocomplete': "off"})
    password = PasswordField('Пароль', [
        DataRequired()], render_kw={'autocomplete': "off"})
    submit = SubmitField('Увійти')


class CreateUser(FlaskForm):
    username = StringField('Юзернейм', [
        DataRequired()])
    email = StringField('Пошта', [
        DataRequired(), Email()])
    name = StringField("Ім'я")
    surname = StringField('Прізвище')
    phone = StringField('Телефон', render_kw={"placeholder": "+3800000000"})
    viber = StringField('Вайбер')
    userType = SelectField('Тип',
                           choices=[
                               ('parent', u'Батьки'),
                               ('admin', u'Адмін'),
                               ('child', u'Учень'),
                               ('teacher', u'Вчитель'),
                               ('tutor', u'Репетитор'),
                               ('zavhoz', u'Завхоз'),
                               ('chef', u'Кухар'),
                               ('accountant', u'Бахгалтер'),
                               ('financist', u'Фінансист'),
                               ('lawyer', u'Юрист'),
                               ('medic', u'Медик'),
                               ('psychologist', u'Психолог')])
    password = PasswordField('Пароль', [
        DataRequired()])
    avatar = FileField('', [
        imageSizeValidator(min=190, max=500, directory=os.path.join('static', 'images', 'avatars')),
        FileAllowed(['jpg', 'png', 'jpeg'], u'Только картинки типов: jpg, png, jpeg!')],
        render_kw={'onchange': "previewFile()", 'class': "addAvatarHidden"},
    )
    submit = SubmitField('Створити')


class CreateTeacherIndividual(FlaskForm):
    studentUsername = StringField(u'Учень(иця)', [DataRequired()],
                                  render_kw={"list": "childrenList", "autocomplete": "off"})
    timeSpent = IntegerField(u'Час (хв)', [DataRequired()], render_kw={"type": "number"})
    lessonDate = DateField(u'Дата уроку', [DataRequired()], render_kw={"type": "date"})
    grade = IntegerField(u'Оцінка', [DataRequired()], render_kw={"type": "number"})
    topic = StringField(u'Тема уроку', [DataRequired()])
    comment = TextAreaField(u'Комментар')
    submit = SubmitField('Створити')


class GetIndividual(FlaskForm):
    timeBefore = DateField(u'До', [Optional()], render_kw={"type": "date"})
    timeAfter = DateField(u'Після', [Optional()], render_kw={"type": "date"})
    teacherUsername = StringField(u'Вчитель', [Optional(), existanceValidator('teacher')], render_kw={"list": "teachersList", "autocomplete": "off"})
    studentUsername = StringField(u'Учень(иця)', [Optional(), existanceValidator('child')],
                                  render_kw={"list": "childrenList", "autocomplete": "off"})
    submit = SubmitField(u'Застосувати')
