from flask import Blueprint, render_template, request, flash, redirect, url_for
from models import Leilao, User, Lance
from database.queries import get_leilao_by_id, get_all_leiloes
from flask_bcrypt import Bcrypt  # Import bcrypt
from flask_login import current_user  # Import current_user
from database import execute_query

bcrypt = Bcrypt()

auction_bp = Blueprint('auction_bp', __name__, template_folder='templates', static_folder='static')

@auction_bp.route("/")
@auction_bp.route("/index")
def index():
    # Obter os leilões mais recentes
    leiloes_recentes_query = "SELECT * FROM leiloes ORDER BY data_inicio DESC LIMIT 4"
    leiloes_recentes = execute_query(leiloes_recentes_query)

    # Obter o leilão com o maior lance atualmente
    leilao_maior_lance_query = "SELECT * FROM leiloes ORDER BY maior_lance DESC LIMIT 1"
    leilao_maior_lance = execute_query(leilao_maior_lance_query)

    # Obter os leilões em destaque (mais visualizados)
    leiloes_destaque_query = "SELECT * FROM leiloes ORDER BY visualizacoes DESC LIMIT 2"
    leiloes_destaque = execute_query(leiloes_destaque_query)

    return render_template(
        "index.html",
        leiloes_recentes=leiloes_recentes,
        leilao_maior_lance=leilao_maior_lance,
        leiloes_destaque=leiloes_destaque,
    )
    
    
@auction_bp.route("/leiloes")
def leiloes():
    leiloes = get_all_leiloes()  # Nova função em queries.py
    return render_template("/leilao/index.html", leiloes=leiloes)


@auction_bp.route("/leiloes/<int:id>/lance")
def get_leilao_by_id(leilao_id):
    query = "SELECT * FROM leiloes WHERE id = %s"
    result = execute_query(query, (leilao_id,))
    return result[0] if result else None

@auction_bp.route("/leiloes/<categoria>")
def leiloes_categoria(categoria):
    query = "SELECT * FROM leiloes WHERE categoria = %s"
    leiloes = execute_query(query, (categoria,))
    return render_template("/leilao/categoria.html", categoria=categoria, leiloes=leiloes)


@auction_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        nome = request.form["nome"]
        email = request.form["email"]
        senha = request.form["senha"]

        # Verificar se o e-mail já está registrado
        query = "SELECT * FROM users WHERE email = %s"
        usuario_existente = execute_query(query, (email,))
        if usuario_existente:
            flash("Email já registrado!", "warning")
        else:
            senha_hash = bcrypt.generate_password_hash(senha).decode("utf-8")
            insert_query = """
                INSERT INTO users (nome, email, senha) 
                VALUES (%s, %s, %s)
            """
            execute_query(insert_query, (nome, email, senha_hash))
            flash("Usuário registrado com sucesso!", "success")
            return redirect(url_for("auth_bp.login"))

    return render_template("sign/register.html")


@auction_bp.route("/dashboard")
def dashboard():
    # Verificar se o usuário está autenticado
    if not current_user.is_authenticated:
        flash("Você precisa estar logado para acessar o dashboard.", "warning")
        return redirect(url_for("auth_bp.login"))

    # Obter dados do usuário
    leiloes_ativos_query = "SELECT * FROM leiloes WHERE criador_id = %s AND status = 'ativo'"
    leiloes_ativos = execute_query(leiloes_ativos_query, (current_user.id,))

    lances_ativos_query = "SELECT * FROM lances WHERE usuario_id = %s"
    lances_ativos = execute_query(lances_ativos_query, (current_user.id,))

    arremates_query = "SELECT * FROM leiloes WHERE vencedor_id = %s"
    arremates = execute_query(arremates_query, (current_user.id,))

    return render_template(
        "dashboard.html",
        current_user=current_user,
        leiloes_ativos=leiloes_ativos,
        lances_ativos=lances_ativos,
        arremates=arremates,
    )

