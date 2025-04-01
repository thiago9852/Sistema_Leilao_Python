from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_bcrypt import Bcrypt
from flask_login import current_user, login_required
from database import execute_query

bcrypt = Bcrypt()

auction_bp = Blueprint('auction_bp', __name__, template_folder='templates', static_folder='static')

@auction_bp.route("/")
@auction_bp.route("/index")
def index():
    try:
        # Obter os leilões mais recentes
        leiloes_recentes = execute_query(
            "SELECT * FROM leilao ORDER BY data_inicio DESC LIMIT 4",
            fetch=True
        )
        
        # Obter o leilão com o maior lance
        leilao_maior_lance = execute_query(
            "SELECT * FROM leilao ORDER BY maior_lance DESC LIMIT 1",
            fetch=True
        )
        
        # Obter leilões em destaque
        leiloes_destaque = execute_query(
            "SELECT * FROM leilao ORDER BY visualizacoes DESC LIMIT 2",
            fetch=True
        )

        return render_template(
            "index.html",
            leiloes_recentes=leiloes_recentes or [],
            leilao_maior_lance=leilao_maior_lance[0] if leilao_maior_lance else None,
            leiloes_destaque=leiloes_destaque or []
        )
        
    except Exception as e:
        flash(f"Erro ao carregar leilões: {str(e)}", "danger")
        return render_template("index.html")

@auction_bp.route("/leiloes")
def leiloes():
    try:
        leiloes = execute_query("SELECT * FROM leilao", fetch=True)
        return render_template("/leilao/index.html", leiloes=leiloes or [])
    except Exception as e:
        flash(f"Erro ao carregar leilões: {str(e)}", "danger")
        return render_template("/leilao/index.html", leiloes=[])

@auction_bp.route("/leiloes/<int:leilao_id>")
def leilao_detalhes(leilao_id):
    try:
        leilao = execute_query(
            "SELECT * FROM leilao WHERE id = %s",
            (leilao_id,),
            fetch=True
        )
        if leilao:
            return render_template("/leilao/show.html", leilao=leilao[0])
        flash("Leilão não encontrado", "warning")
        return redirect(url_for("auction_bp.leiloes"))
    except Exception as e:
        flash(f"Erro ao carregar leilão: {str(e)}", "danger")
        return redirect(url_for("auction_bp.leiloes"))

@auction_bp.route("/leiloes/<categoria>")
def leiloes_categoria(categoria):
    try:
        leiloes = execute_query(
            "SELECT * FROM leilao WHERE categoria = %s",
            (categoria,),
            fetch=True
        )
        return render_template(
            "/leilao/categoria.html",
            categoria=categoria,
            leiloes=leiloes or []
        )
    except Exception as e:
        flash(f"Erro ao carregar leilões: {str(e)}", "danger")
        return render_template("/leilao/categoria.html", categoria=categoria, leiloes=[])

@auction_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        try:
            nome = request.form["nome"]
            email = request.form["email"]
            senha = request.form["senha"]

            # Verificar se o e-mail já está registrado
            usuario_existente = execute_query(
                "SELECT id FROM users WHERE email = %s",
                (email,),
                fetch=True
            )
            
            if usuario_existente:
                flash("Email já registrado!", "warning")
            else:
                senha_hash = bcrypt.generate_password_hash(senha).decode("utf-8")
                execute_query(
                    "INSERT INTO users (nome, email, senha) VALUES (%s, %s, %s)",
                    (nome, email, senha_hash)
                )
                flash("Usuário registrado com sucesso!", "success")
                return redirect(url_for("auth_bp.login"))
                
        except Exception as e:
            flash(f"Erro no registro: {str(e)}", "danger")

    return render_template("sign/register.html")

@auction_bp.route("/dashboard")
@login_required
def dashboard():
    try:
        leiloes_ativos = execute_query(
            "SELECT * FROM leilao WHERE criador_id = %s AND status = 'ativo'",
            (current_user.id,),
            fetch=True
        )
        
        lances_ativos = execute_query(
            "SELECT * FROM lance WHERE usuario_id = %s",
            (current_user.id,),
            fetch=True
        )
        
        arremates = execute_query(
            "SELECT * FROM leilao WHERE vencedor_id = %s",
            (current_user.id,),
            fetch=True
        )

        return render_template(
            "dashboard.html",
            current_user=current_user,
            leiloes_ativos=leiloes_ativos or [],
            lances_ativos=lances_ativos or [],
            arremates=arremates or []
        )
        
    except Exception as e:
        flash(f"Erro ao carregar dashboard: {str(e)}", "danger")
        return render_template("dashboard.html")