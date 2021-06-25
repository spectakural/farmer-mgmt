from flask import Flask
from flask_wtf import CSRFProtect
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)
app.config['SECRET_KEY'] = '627836bv278v6bo3bwjbhev'
CORS(app, resources={r'/*': {'origins': '*'}})

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)

# this view doesnt exist create a login page and put the function name below
login_manager.login_view = 'index'

csrf = CSRFProtect(app)
from flask_gen import routes
