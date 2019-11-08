from flask import Flask, session
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
bcrypt = Bcrypt(app)
cwd = os.getcwd()

file = cwd + '/spell/security/test.db'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + file
db = SQLAlchemy(app)

from spell.userman import Users
from spell.userman import User

app.config['host'] = "0.0.0.0"
app.config['port'] = "5000"
app.config['debug'] = "True"
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'

app.config['WTF_CSRF_ENABLED'] = False

from spell import urls

#Users.load_users()
