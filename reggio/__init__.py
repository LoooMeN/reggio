from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from werkzeug.security import generate_password_hash

db_type = 'mysql'
db_login = 'italent7_test'
db_pass = 'aws777awe878'
db_host = 'italent7.mysql.tools'
db_name = 'italent7_test'
connection_string = '%s://%s:%s@%s/%s' % (db_type, db_login, db_pass, db_host, db_name)
app = Flask(__name__)
app.secret_key = b'VALERUSBLADISFTW'
app.config['SQLALCHEMY_DATABASE_URI'] = connection_string
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
login_manager = LoginManager(app)

from reggio.models import User
from reggio import routes

db.create_all()

if not User.query.filter_by(userType='superAdmin').first():
    admin = User(username='admin', email='looomen@hotmail.com', userType='superAdmin', password=generate_password_hash('123'))
    db.session.add(admin)
    db.session.commit()
