import os
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)


@app.route("/")
def home():
	return render_template("index.html")

@app.route("/credentials", methods=["GET"])
def get_od_credentials():
	first_name = request.headers.get('X-AppleConnect-FirstName')
	last_name = request.headers.get('X-AppleConnect-LastName')
	return str(request.headers)#str(first_name) + " " + str(last_name)


if __name__ == "__main__":
	port = int(os.environ.get("PORT", 5000))
	#app.run(debug=True)
	app.run(host='0.0.0.0', port=port)
