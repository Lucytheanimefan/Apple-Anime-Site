from commons import db


class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)

    mal_user = db.relationship("MalUser", uselist=False, back_populates="user")

    def __init__(self, username):
        self.username = username

    def __repr__(self):
        return '<User %r>' % self.username
