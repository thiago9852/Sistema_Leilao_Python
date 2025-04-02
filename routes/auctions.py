from flask import Blueprint, render_template, request, flash, redirect, url_for, current_app
from flask_bcrypt import Bcrypt
from flask_login import current_user, login_required
from database import execute_query
from datetime import datetime
import time
import os
from query.queries import get_leiloes_veiculos, get_leiloes_imoveis, get_leiloes_outros
from werkzeug.utils import secure_filename
from models import db, Leilao, Lance, User
from sqlalchemy import func, and_

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
        flash(f"Erro ao carregar os leilões: {str(e)}", "danger")
        return render_template("index.html")


@auction_bp.route("/leiloes/dashboard/novo", methods=["GET", "POST"])
@login_required
def criar_leilao():
    if request.method == "GET":
        return render_template("leilao/criar_leilao.html")

    try:
        # Processamento do arquivo de imagem
        file = request.files.get('imagem')
        if not file or file.filename == '':
            flash('Nenhuma imagem selecionada', 'danger')
            return render_template("leilao/criar_leilao.html")
        
        # Cria diretório se não existir
        os.makedirs(current_app.config['UPLOAD_FOLDER'], exist_ok=True)
        
        filename = secure_filename(f"{current_user.id}_{int(time.time())}.{file.filename.rsplit('.', 1)[1].lower()}")
        filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
            
        # Salva arquivo
        file.save(filepath)
        imagem_url = os.path.join(filename)

        # Query
        query = """
            INSERT INTO leilao (
                item, descricao, sobre, lance_inicial, lance_minimo, lance_maximo, 
                data_inicio, data_fim, categoria, criador_id, status, imagem_url
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 'ativo', %s)
        """
        
        params = (
            request.form["item"],
            request.form["descricao"],
            request.form.get("sobre", ""),
            float(request.form["lance_inicial"]),
            float(request.form.get("lance_minimo", 0)),
            float(request.form.get("lance_maximo", 0)),
            datetime.strptime(request.form["data_inicio"], "%Y-%m-%dT%H:%M"),
            datetime.strptime(request.form["data_fim"], "%Y-%m-%dT%H:%M"),
            request.form["categoria"],
            current_user.id,
            imagem_url
        )

        execute_query(query, params)
        flash("Leilão criado com sucesso!", "success")
        return redirect(url_for("auction_bp.dashboard"))

    except Exception as e:
        flash(f"Erro ao criar leilão: {str(e)}", "danger")
        return redirect(url_for("auction_bp.criar_leilao"))


@auction_bp.route("/leiloes")
def leiloes():
    try:
        # Consulta para veículos
        veiculos = db.session.query(
            Leilao,
            func.coalesce(
                db.session.query(func.max(Lance.valor))
                .filter(Lance.leilao_id == Leilao.id)
                .scalar_subquery(),
                Leilao.lance_inicial
            ).label('maior_lance'),
            db.session.query(User.nome)
                .join(Lance, Lance.usuario_id == User.id)
                .filter(Lance.leilao_id == Leilao.id)
                .order_by(Lance.valor.desc())
                .limit(1)
                .scalar_subquery().label('maior_lance_user')
        ).filter(
            Leilao.categoria == 'veiculos',
            Leilao.status == 'ativo',
            Leilao.data_inicio <= datetime.now()
        ).order_by(Leilao.data_inicio.desc()).limit(4).all()

        # Consulta para imóveis
        imoveis = db.session.query(
            Leilao,
            func.coalesce(
                db.session.query(func.max(Lance.valor))
                .filter(Lance.leilao_id == Leilao.id)
                .scalar_subquery(),
                Leilao.lance_inicial
            ).label('maior_lance'),
            db.session.query(User.nome)
                .join(Lance, Lance.usuario_id == User.id)
                .filter(Lance.leilao_id == Leilao.id)
                .order_by(Lance.valor.desc())
                .limit(1)
                .scalar_subquery().label('maior_lance_user')
        ).filter(
            Leilao.categoria == 'imoveis',
            Leilao.status == 'ativo',
            Leilao.data_inicio <= datetime.now()
        ).order_by(Leilao.data_inicio.desc()).limit(4).all()

        # Consulta para outros itens
        outros = db.session.query(
            Leilao,
            func.coalesce(
                db.session.query(func.max(Lance.valor))
                .filter(Lance.leilao_id == Leilao.id)
                .scalar_subquery(),
                Leilao.lance_inicial
            ).label('maior_lance'),
            db.session.query(User.nome)
                .join(Lance, Lance.usuario_id == User.id)
                .filter(Lance.leilao_id == Leilao.id)
                .order_by(Lance.valor.desc())
                .limit(1)
                .scalar_subquery().label('maior_lance_user')
        ).filter(
            Leilao.categoria == 'outros',
            Leilao.status == 'ativo',
            Leilao.data_inicio <= datetime.now()
        ).order_by(Leilao.data_inicio.desc()).limit(4).all()

        # Formatar os resultados
        def formatar_leiloes(leiloes):
            return [{
                'id': leilao.id,
                'item': leilao.item,
                'descricao': leilao.descricao,
                'sobre': leilao.sobre,
                'lance_inicial': float(leilao.lance_inicial),
                'maior_lance': float(maior_lance),
                'maior_lance_user': maior_lance_user,
                'imagem_url': leilao.imagem_url,
                'data_fim': leilao.data_fim
            } for leilao, maior_lance, maior_lance_user in leiloes]

        return render_template(
            "/leilao/index.html",
            categoria_veiculos=formatar_leiloes(veiculos),
            categoria_imoveis=formatar_leiloes(imoveis),
            categoria_outros=formatar_leiloes(outros)
        )

    except Exception as e:
        flash(f"Erro ao carregar leilões: {str(e)}", "danger")
        return render_template(
            "/leilao/index.html",
            categoria_veiculos=[],
            categoria_imoveis=[],
            categoria_outros=[]
        )


@auction_bp.route("/leiloes/<categoria>")
def leiloes_categoria(categoria):
    try:
        leiloes = execute_query(
            "SELECT * FROM leilao WHERE categoria = %s",
            (categoria,),
            fetch=True
        )
        return render_template(
            "/leilao/leilao_categoria.html",
            categoria=categoria,
            leiloes=leiloes or []
        )
    except Exception as e:
        flash(f"Erro carregar leilões: {str(e)}", "danger")
        return render_template("/leilao/leilao_categoria.html", categoria=categoria, leiloes=[])



@auction_bp.route("/leiloes/<int:leilao_id>")
def leilao_show(leilao_id):
    try:
        leilao = execute_query(
            """
            SELECT leilao.*, 
                user.nome AS nome_criador,
                COALESCE(lance.valor, leilao.lance_inicial) AS lance_atual,
                lance.usuario_id AS maior_lance_user_id,
                u.nome AS maior_lance_user
            FROM leilao
            JOIN user ON leilao.criador_id = user.id
            LEFT JOIN lance ON leilao.id = lance.leilao_id
            LEFT JOIN user u ON lance.usuario_id = u.id
            WHERE leilao.id = %s
            ORDER BY lance.valor DESC
            LIMIT 1
            """,
            (leilao_id,),
            fetch=True
        )


        if leilao:
            return render_template("/leilao/show.html", leilao=leilao[0])
        flash("Leilão não encontrado", "warning")
        return redirect(url_for("auction_bp.leiloes"))
    except Exception as e:
        flash(f"Erro, não foi possível carregar leilão: {str(e)}", "danger")
        return redirect(url_for("auction_bp.leiloes"))
    
    
    
@auction_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        try:
            nome = request.form["nome"]
            email = request.form["email"]
            senha = request.form["senha"]

            # Verificar se o e-mail já está registrado
            usuario_existente = execute_query(
                "SELECT id FROM user WHERE email = %s",
                (email,),
                fetch=True
            )
            
            if usuario_existente:
                flash("Email já registrado!", "warning")
            else:
                senha_hash = bcrypt.generate_password_hash(senha).decode("utf-8")
                execute_query(
                    "INSERT INTO user (nome, email, senha) VALUES (%s, %s, %s)",
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
    leiloes_ativos = []
    lances_ativos = []
    arremates = []
    
    try:
        leiloes_ativos = execute_query(
            "SELECT * FROM leilao WHERE criador_id = %s",
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
            leiloes_ativos=leiloes_ativos,
            lances_ativos=lances_ativos,
            arremates=arremates
        )
        
    except Exception as e:
        flash(f"Erro ao carregar dashboard: {str(e)}", "danger")
        return render_template("dashboard.html")