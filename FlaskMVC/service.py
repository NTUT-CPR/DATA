from flask import Flask, Blueprint
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = \
    'mysql+pymysql://root:db123456@localhost/DBMS'
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SECRET_KEY'] = '908a561008fd5f88a3a86e20add4ab3f'
app.config['PROPAGATE_EXCEPTIONS'] = True

db = SQLAlchemy(app)

blueprint = {'index': Blueprint('index', __name__),
             'admin': Blueprint('admin', __name__)}


def get_blueprint(key):
    return blueprint[key]

login_manager = LoginManager()
login_manager.login_view = 'index.index'
