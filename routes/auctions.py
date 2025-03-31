
# auction.py

from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required
from models import Leilao  # Importe o modelo de Leilão (ou como você nomeou o modelo)
from flask_bcrypt import Bcrypt  # Importando o Bcrypt para hash de senhas

bcrypt = Bcrypt()

auction_bp = Blueprint('auction_bp', __name__, template_folder='templates', static_folder='static')

@auction_bp.route("/leiloes")
def leiloes():
    # pegar os leilões do banco de dados e passar para o template
    leiloes = Leilao.query.all()
    return render_template("/leilao/index.html", leiloes=leiloes)

@auction_bp.route("/leiloes/<int:id>/lance")
def leiloes_show(id):
    # pega um leilão específico para mostrar detalhes
    leilao = Leilao.query.get(id)
    return render_template("/leilao/show.html", leilao=leilao)

@auction_bp.route("/leiloes/<categoria>")
def leiloes_categoria(categoria):
    # Filtrando leilões por categoria
    leiloes = Leilao.query.filter_by(categoria=categoria).all()
    return render_template("/leilao/categoria.html", categoria=categoria, leiloes=leiloes)


@auction_bp.route("/")
@auction_bp.route("/index")
def index():
    return render_template("index.html")


@auction_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        nome = request.form["nome"]
        email = request.form["email"]
        senha = request.form["senha"]

        if any(user['email'] == email for user in users):
            flash("Email já registrado!", "warning")
        else:
            senha_hash = bcrypt.generate_password_hash(senha).decode("utf-8")
            users.append({"nome": nome, "email": email, "senha": senha_hash})
            flash("Usuário registrado com sucesso!", "success")
            return redirect(url_for("login"))

    return render_template("sign/register.html")
