import os
from flask import Flask, render_template, request

app = Flask(__name__)


@app.route("/")
def home():
	return render_template("index.html")

@app.route("/credentials", methods=["GET"])
def get_od_credentials():
	request.headers.get('X-AppleConnect-FirstName')
	first_name = request.headers['X-AppleConnect-FirstName']
	request.headers.get('X-AppleConnect-LastName')
	last_name = request.headers['X-AppleConnect-LastName']
	return first_name + " " + last_name


if __name__ == "__main__":
	port = int(os.environ.get("PORT", 5000))
	#app.run(debug=True)
	app.run(host='0.0.0.0', port=port)
