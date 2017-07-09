import os
from flask import Flask, render_template, request, escape
from commons import db
from models import common, mal
import coordinators

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://localhost/tkatzenbaer'
db.init_app(app)

with app.app_context():
    # Extensions like Flask-SQLAlchemy now know what the "current" app
    # is while within this block. Therefore, you can now run........
    db.create_all()


def get_apple_user():
    dsid = request.headers.get('X-AppleConnect-PersonId')
    # Debugging Code
    if not dsid:
        dsid = os.environ.get('X-AppleConnect-PersonId')
    user = common.User.query.filter_by(dsid=dsid).first()
    """:type: common.User"""
    if not user:
        user = common.User(dsid)
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


@app.route("/mal/update/<username>")
def mal_page(username):
    if not username:
        username = 'katzenbaer'

    coordinator = coordinators.MalCoordinator()
    animelist = coordinator.fetch_animelist(username)

    if not animelist:
        return u"Error while fetching top anime for {}".format(username)
    else:
        try:
            mal_user = mal.MalUser.query.filter_by(username=username).first()
            """:type: mal.MalUser"""

            if mal_user:
                db.session.query(mal.MalEntry).filter_by(mal_user=mal_user).delete()
            else:
                mal_user = mal.MalUser(username)
                db.session.add(mal_user)

            mal_user.entries.extend(animelist)

            db.session.add(mal_user)
            db.session.add_all(animelist)
        finally:
            db.session.commit()

        top_anime = coordinator.filter_top_anime(animelist)
        return render_template("mal_user.html", top_anime = top_anime, username=username)
        #return u"{}'s top anime: {}".format(username, ', '.join(list(top_anime)))


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


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True)
    #app.run(host='0.0.0.0', port=port)
