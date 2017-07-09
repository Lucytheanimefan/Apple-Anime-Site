from commons import db


class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    dsid = db.Column(db.Integer, unique=True)

    mal_user = db.relationship("MalUser", uselist=False, back_populates="user",
                               cascade="all, delete-orphan")
    """:type: models.mal.MalUser"""

    def __init__(self, dsid):
        self.dsid = dsid

    def __repr__(self):
        return '<User %r>' % self.dsid
