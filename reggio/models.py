from flask_login import UserMixin

from reggio import db, login_manager

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True, unique=True)
    username = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    userType = db.Column(db.String(80), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    nickname = 'default'



@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)