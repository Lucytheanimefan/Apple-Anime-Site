import os
 
import hashlib

from flask import Flask, render_template, request, escape
from sqlalchemy import func
import flask
from flask import Flask, render_template, request, jsonify, send_file, escape
import coordinators
from commons import db
from models import common, mal

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://localhost/lucyzhang'#tkatzenbaer'
db.init_app(app)

with app.app_context():
    # Extensions like Flask-SQLAlchemy now know what the "current" app
    # is while within this block. Therefore, you can now run........
    db.create_all()


def get_apple_user():
    email = request.headers.get('X-AppleConnect-EmailAddress',
                                os.environ.get('X-AppleConnect-EmailAddress'))

    email_hash = hashlib.sha256(email).hexdigest()
    user = common.User.query.filter_by(email_hash=email_hash).first()
    """:type: common.User"""
    if not user:
        user = common.User(email=email)
        db.session.add(user)
        db.session.commit()
    return user


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/mal/link/<username>")
def link_mal_user(username):
    user = get_apple_user()
    if user.mal_user and user.mal_user.username == username:
        return escape(u"Already linked to {}!".format(repr(user.mal_user)))

    mal.MalUser.query.filter_by(username=username).delete()

    mal_user = mal.MalUser(username, user)
    db.session.add(user)
    db.session.add(mal_user)
    db.session.commit()
    return escape(u"Linked {} to {}!".format(repr(user), repr(mal_user)))


@app.route("/mal/update")
def mal_update():
    user = get_apple_user()

    if not user.mal_user:
        return u"Please link a MyAnimeList account first."

    coordinator = coordinators.MalCoordinator()
    animelist = coordinator.fetch_animelist(user)

    if not animelist:
        return u"Error while fetching top anime for {}".format(user.mal_user.username)
    else:
        db.session.query(mal.MalEntry).filter_by(mal_user=user.mal_user).delete()

        user.mal_user.entries.extend(animelist)

        db.session.add(user.mal_user)
        db.session.commit()

        return u"Successfully updated entries for {}".format(user.mal_user.username)


@app.route("/mal/top-this-season")
def mal_top_season():
    sum_watched_episodes = func.sum(mal.MalEntry.watched_episodes).label("sum_watched_ep")
    subquery = db.session.query(mal.MalEntry.anime_id.label('aid'), sum_watched_episodes)\
        .group_by(mal.MalEntry.anime_id)\
        .filter_by(airing_status=mal.MalEntryAiringStatus.airing)\
        .order_by(sum_watched_episodes.desc()).subquery()
    subquery = db.session.query(subquery).filter(subquery.c.sum_watched_ep > 0).subquery()
    subquery = db.session.query(subquery, mal.MalEntry)\
        .distinct(mal.MalEntry.title)\
        .join(mal.MalEntry, mal.MalEntry.anime_id == subquery.c.aid)\
        .order_by(mal.MalEntry.title).subquery()
    entries = db.session.query(subquery)\
        .order_by(subquery.c.sum_watched_ep.desc()).all()
    """:type: list[mal.MalEntry]"""

    if not entries:
        return u"No records."

    titles = [u"{} - {}".format(e.title, e.sum_watched_ep) for e in entries]
    return u"Top anime this season @ Apple: {}".format(', '.join(titles))


@app.route("/mal/top/<username>")
def mal_top(username):
    coordinator = coordinators.MalCoordinator()

    mal_user = mal.MalUser.query.filter_by(username=username).first()
    """:type: mal.MalUser|None"""

    if not mal_user:
        return u"No records for {}".format(username)

    top_anime = coordinator.filter_top_anime(mal_user.entries)
    return render_template("mal_user.html", top_anime = top_anime, username=username)


@app.route("/credentials", methods=["GET"])
def get_od_credentials():
	name = request.headers.get('X-Forwarded-User')
	return str(name)

@app.route("/signin", methods=["POST"])
def signin():
    username = request.form["malUsername"]#TODO: do something with username
    return home()

@app.route("/login")
def login():
    return render_template("login.html")


@app.route("/footer/<footer_category>/")
def footer_pages(footer_category):
    # TODO: do something for this
    return flask.redirect("http://24.media.tumblr.com/a958e89157a9b23950059aaa5acf2be2/tumblr_myfqb93rcs1spfncwo1_400.gif")



if __name__ == "__main__":
    port = os.environ.get("PORT_WEB")
    print "PORT: "
    print port
    if port:
        app.run(host='0.0.0.0', port=int(port))
    else:
        app.run(debug=True)
