import os
from flask import Flask, render_template, request, jsonify
from commons import db
import coordinators

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://localhost/tkatzenbaer'
# db.init_app(app)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/mal/")
@app.route("/mal/<username>")
def mal_page(username=None):
    if not username:
        username = 'katzenbaer'

    coordinator = coordinators.MalCoordinator()
    animelist = coordinator.fetch_animelist(username)
    if isinstance(animelist, dict):
        return u"Error while fetching top anime for {}".format(username)
    else:
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
