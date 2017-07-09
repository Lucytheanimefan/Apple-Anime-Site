from commons import db
import hashlib


class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    email_hash = db.Column(db.String(80), unique=True)

    mal_user = db.relationship("MalUser", uselist=False, back_populates="user",
                               cascade="all, delete-orphan")
    """:type: models.mal.MalUser"""

    def __init__(self, email):
        # TODO: Make hashing stronger
        self.email_hash = hashlib.sha256(email).hexdigest()

    def __repr__(self):
        return '<User %r>' % self.id
