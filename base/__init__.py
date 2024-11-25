import warnings
from datetime import timedelta

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.secret_key = '3w4e6t7by8nh9jm0kbvufjifi4'

warnings.filterwarnings("ignore", category=FutureWarning)
warnings.filterwarnings("ignore", category=DeprecationWarning)

app.config['SQLALCHEMY_ECHO'] = True

app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=30)

app.config['SQLALCHEMY_DATABASE_URI'] = \
    'mysql+pymysql://root:Divpatel_2403@localhost:3306/lms_moodle_update'

app.config['SQLALCHEMY_MAX_OVERFLOW'] = 0

app.config['JSONIFY_PRETTYPRINT_REGULAR'] = False
db = SQLAlchemy(app)

from base.com import controller


# from flask import Flask,render_template, request
# from flask_mysqldb import MySQL
 
# app = Flask(__name__)
 
# app.config['MYSQL_HOST'] = 'localhost'
# app.config['MYSQL_USER'] = 'root'
# app.config['MYSQL_PASSWORD'] = ''
# app.config['MYSQL_DB'] = 'flask'
 
# mysql = MySQL(app)