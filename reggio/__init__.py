from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

from reggio.secret import *


connection_string = '%s://%s:%s@%s/%s' % (db_type, db_login, db_pass, db_host, db_name)
app = Flask(__name__, instance_path='/home/looomen/Desktop/reggio/reggio')
app.secret_key = secret_key
app.config['SQLALCHEMY_DATABASE_URI'] = connection_string
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
login_manager = LoginManager(app)
from reggio import routes