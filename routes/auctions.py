from flask import Blueprint, render_template, request, flash, redirect, url_for
from models import Leilao, User, Lance  # Import the Leilao, User, and Lance models
from database.queries import get_leilao_by_id, get_all_leiloes
from flask_bcrypt import Bcrypt  # Import bcrypt
from flask_login import current_user  # Import current_user
from database import db_session  # Import db_session

bcrypt = Bcrypt()

auction_bp = Blueprint('auction_bp', __name__, template_folder='templates', static_folder='static')

@auction_bp.route("/leiloes")
def leiloes():
    leiloes = get_all_leiloes()  # Nova função em queries.py
    return render_template("/leilao/index.html", leiloes=leiloes)


@auction_bp.route("/leiloes/<int:id>/lance")
def leiloes_show(id):
    leilao = get_leilao_by_id(id)
    return render_template("/leilao/show.html", leilao=leilao)

@auction_bp.route("/leiloes/<categoria>")
def leiloes_categoria(categoria):
    # Filtrando leilões por categoria
    leiloes = Leilao.query.filter_by(categoria=categoria).all()
    return render_template("/leilao/categoria.html", categoria=categoria, leiloes=leiloes)

@auction_bp.route("/")
@auction_bp.route("/index")
def index():
    # Obter os leilões mais recentes
    leiloes_recentes = Leilao.query.order_by(Leilao.data_inicio.desc()).limit(4).all()

    # Obter o leilão com o maior lance atualmente
    leilao_maior_lance = Leilao.query.order_by(Leilao.maior_lance.desc()).first()

    # Obter os leilões em destaque (mais visualizados)
    leiloes_destaque = Leilao.query.order_by(Leilao.visualizacoes.desc()).limit(2).all()

    leilao_sort = Leilao.query.sort_by(Leilao.id).limit(1).all()
    
    return render_template(
        "index.html",
        leiloes_recentes=leiloes_recentes,
        leilao_maior_lance=leilao_maior_lance,
        leiloes_destaque=leiloes_destaque,
        leilao_sort=leilao_sort,
    )

@auction_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        nome = request.form["nome"]
        email = request.form["email"]
        senha = request.form["senha"]

        # Verificar se o e-mail já está registrado
        usuario_existente = db_session.query(User).filter_by(email=email).first()
        if usuario_existente:
            flash("Email já registrado!", "warning")
        else:
            senha_hash = bcrypt.generate_password_hash(senha).decode("utf-8")
            novo_usuario = User(nome=nome, email=email, senha=senha_hash)
            db_session.add(novo_usuario)
            db_session.commit()
            flash("Usuário registrado com sucesso!", "success")
            return redirect(url_for("login"))

    return render_template("sign/register.html")

@auction_bp.route("/dashboard")
def dashboard():
    # Verificar se o usuário está autenticado
    if not current_user.is_authenticated:
        flash("Você precisa estar logado para acessar o dashboard.", "warning")
        return redirect(url_for("auth_bp.login"))

    # Obter dados do usuário
    leiloes_ativos = Leilao.query.filter_by(criador_id=current_user.id, status="ativo").all()
    lances_ativos = Lance.query.filter_by(usuario_id=current_user.id).all()
    arremates = Leilao.query.filter_by(vencedor_id=current_user.id).all()

    return render_template(
        "dashboard.html",
        current_user=current_user,
        leiloes_ativos=leiloes_ativos,
        lances_ativos=lances_ativos,
        arremates=arremates,
    )

