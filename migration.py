import hashlib
import random
import string
from datetime import datetime

from FlaskMVC.service import app, db
from FlaskMVC.models.db.StreamKey import StreamKey


def create_data():

    # Add Admin Data

    key_1 = StreamKey(key_id='ICEiIyQlJicoKSorLC0uLw==', key='FRYXGBkaGxwdHh8gISIjJA==', session_id='AAAAAAAAAAAA', stream_id=123)
    db.session.add_all([key_1])
    db.session.commit()
