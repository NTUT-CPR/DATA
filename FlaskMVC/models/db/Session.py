from FlaskMVC.service import db


class Session(db.Model):

    __tablename__ = "sessions"
    session_id = db.Column(db.String(32), primary_key=True)
    user_id = db.Column(db.String(64))
    expiry = db.Column(db.DateTime)

    def __repr__(self):
        return '<Session %r>' % self.session_id
