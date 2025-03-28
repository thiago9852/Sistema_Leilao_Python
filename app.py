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

@app.route("/leiloes/<categoria>")
def leiloes_categoria(categoria):
    categorias_disponiveis = ["veiculos", "imoveis", "eletronicos"]
    
    if categoria not in categorias_disponiveis:
        return "Categoria não encontrada", 404
    
    return render_template("leiloes_categoria.html", categoria=categoria)

@app.route("/login")
def login():
	return render_template("/sign/login.html")

@app.route("/register")
def register():
	return render_template("/sign/register.html")


if __name__ == '__main__':
	app.run(debug=True, host='0.0.0.0', port=5000)