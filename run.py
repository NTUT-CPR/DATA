# -*- coding: utf-8 -*-
import sys

from flask.ext.login import current_user

from migration import create_data
from FlaskMVC.service import app, db, login_manager, get_blueprint
from FlaskMVC.models.db.User import User, AccessLevel
from FlaskMVC.models.db.Session import Session

@login_manager.user_loader
def user_loader(user_id):
    return User.query.get(user_id)

login_manager.init_app(app)


@app.context_processor
def context_processor():
    return dict(current_user=current_user, AccessLevel=AccessLevel)

app.register_blueprint(get_blueprint('index'), url_prefix='/api')
app.register_blueprint(get_blueprint('admin'), url_prefix='/admin')
app.register_blueprint(get_blueprint('dash'), url_prefix='/dash')

if __name__ == '__main__':
    if len(sys.argv) > 1:
        if sys.argv[1] == 'create_db':
            if len(sys.argv) > 2 and sys.argv[2] == 'drop':
                db.drop_all()
                print("Droped.")
            db.create_all()
            print("Done.")
        if sys.argv[1] == 'create_data':
            create_data()
            print("Done.")

    else:
        app.run(host='0.0.0.0', debug=True)
