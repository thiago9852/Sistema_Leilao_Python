from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
@app.route("/index")
def index():
	return render_template("index.html")

@app.route("/dashboard")
def countTimer():
	return render_template("dashboard.html")

@app.route("/leiloes")
def leiloes():
	return render_template("leiloes.html")

@app.route("/login")
def login():
	return render_template("/sign/login.html")

if __name__ == '__main__':
	app.run(debug=True)