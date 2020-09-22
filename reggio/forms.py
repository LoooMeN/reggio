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
from reggio.models import Child


def imageSizeValidator(min=-1, max=-1, directory='static'):
    sizeMessage = u"Фото должно быть не меньше %d и не больше %d пикселей по обоим параметрам." % (min, max)
    nameMessage = u"Фото с таким именем уже существует, переименуйте его пожалуйста."
    

    def _imageSizeValidator(form, field):
        f = field.data
        if f:
            filename = secure_filename(f.filename)
            filepath = os.path.join(
                app.instance_path, directory, filename
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
    username = StringField('Username', [
        DataRequired()])
    password = PasswordField('Password', [
        DataRequired()])
    submit = SubmitField('Submit')

class CreateUser(FlaskForm):
    username = StringField('Username', [
        DataRequired()])
    email = StringField('Email', [
        DataRequired(), Email()])
    name = StringField('Name')
    surname = StringField('Surname')
    phone = StringField('phone', render_kw={"placeholder": "+3800000000"})
    viber = StringField('viber')
    userType = SelectField('Type',
        choices=[
            ('parent', u'Родитель'),
            ('admin', u'Админ'),
            ('child', u'Ребёнок'),
            ('teacher', u'Преподаватель'),
            ('tutor', u'Тьютор'),
            ('zavhoz', u'Завхоз'),
            ('chef', u'Повар'),
            ('accountant', u'Бахгалтер'),
            ('financist', u'Финансист'),
            ('lawyer', u'Юрист'),
            ('medic', u'Медик'),
            ('psychologist', u'Психолог')])
    password = PasswordField('Password', [
        DataRequired()])
    avatar = FileField('image', [
        imageSizeValidator(min=190, max=500, directory=os.path.join('static', 'images', 'avatars')),
        FileAllowed(['jpg', 'png', 'jpeg'], u'Только картинки типов: jpg, png, jpeg!')
    ])
    submit = SubmitField('Submit')

class CreateTeacherIndividual(FlaskForm):
    studentUsername = StringField(u'Ученик(ца)', [DataRequired()], render_kw={"list": "childrenList"})
    timeSpent = IntegerField(u'Потраченное время (в минутах)', [DataRequired()], render_kw={"type": "number"})
    lessonDate = DateField(u'Дата урока', [DataRequired()], render_kw={"type": "date"})
    grade = IntegerField(u'Оценка', [DataRequired()], render_kw={"type": "number"})
    topic = StringField(u'Тема урока', [DataRequired()])
    comment = TextAreaField(u'Комментарий к уроку')
    submit = SubmitField('Submit')
