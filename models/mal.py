import enum

from commons import db


class MalUser(db.Model):
    __tablename__ = 'mal_user'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80))

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship("User", back_populates="mal_user")

    entries = db.relationship("MalEntry", back_populates="mal_user")

    def __init__(self, username, user=None):
        self.username = username
        self.user = user

    def __repr__(self):
        return '<MalUser {}>'.format(self.username)


class MalEntryUserStatus(enum.Enum):
    watching = 1
    completed = 2
    on_hold = 3
    dropped = 4
    plan_to_watch = 6


class MalEntryAiringStatus(enum.Enum):
    airing = 1
    aired = 2
    not_aired = 3


class MalEntry(db.Model):
    __tablename__ = 'mal_entry'

    id = db.Column(db.Integer, primary_key=True)

    mal_user_id = db.Column(db.Integer, db.ForeignKey('mal_user.id'))
    mal_user = db.relationship("MalUser", back_populates="entries")

    anime_id = db.Column(db.Integer)
    title = db.Column(db.String(80))
    user_status = db.Column(db.Enum(MalEntryUserStatus))
    airing_status = db.Column(db.Enum(MalEntryAiringStatus))
    watched_episodes = db.Column(db.Integer)
    total_episodes = db.Column(db.Integer)
    user_score = db.Column(db.Integer)

    def __repr__(self):
        mal_username = self.mal_user.username if self.mal_user else ''
        return '<{}:MalEntry {} - {} - {} - {}/{}>'.format(mal_username, self.title,
                                                           self.airing_status.name,
                                                           self.user_status.name,
                                                           self.watched_episodes,
                                                           self.total_episodes)
