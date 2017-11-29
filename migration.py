import hashlib
import random
import string
from datetime import datetime

from FlaskMVC.service import app, db
from FlaskMVC.models.db.User import User


def create_data():

    # Add Admin Data
    pw1 = hashlib.sha256('1234'.encode('ascii')).hexdigest()

    adm_1 = User(account='admin', password=pw1, level=1, name='Admin')
    db.session.add_all([adm_1])
    db.session.commit()
