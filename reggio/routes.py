from flask import render_template, url_for, request, flash, redirect
from werkzeug.security import check_password_hash
from flask_login import current_user, login_user, logout_user

from reggio import app, db
from reggio.models import User


@app.route('/')
def main():
    if current_user.is_authenticated:
        return render_template('child.html', user=current_user.username.upper())
    return render_template('tsar.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    username = request.form.get('username') 
    password = request.form.get('password')

    if username and password:
        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('main'))
        else:
            flash('Incorrect credentials, homie')
    else:
        flash('Please fill the fields, homie')
    return render_template('login.html')

@app.route('/logout', methods=['GET', 'POST'])
def logout():
    if current_user:
        logout_user()
    return redirect(url_for('main'))
