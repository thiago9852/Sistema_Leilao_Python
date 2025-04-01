# routes/auth.py

from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user, login_required
from models.user import User
from flask_bcrypt import Bcrypt
from models import db


# Criação da Blueprint para autenticação
auth_bp = Blueprint('auth', __name__, template_folder='templates', static_folder='static')

bcrypt = Bcrypt()

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        senha = request.form["senha"]
        user = User.query.filter_by(email=email).first()

        if user and bcrypt.check_password_hash(user.senha, senha):
            login_user(user)
            flash("Login bem-sucedido!", "success")
            return redirect(url_for("auction.index"))  # Redireciona para a página de leilões
        else:
            flash("Credenciais inválidas.", "danger")

    return render_template("login.html")

@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Logout realizado.", "info")
    return redirect(url_for("auction.index"))  # Redireciona para a página inicial

@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        email = request.form["email"]
        senha = request.form["senha"]
        
        # Verifica se usuário já existe
        if User.query.filter_by(email=email).first():
            flash("Email já cadastrado.", "danger")
            return redirect(url_for("auth.register"))
        
        # Cria novo usuário
        hashed_password = bcrypt.generate_password_hash(senha).decode('utf-8')
        new_user = User(username=username, email=email, senha=hashed_password)
        
        db.session.add(new_user)
        db.session.commit()
        
        flash("Registro realizado com sucesso! Faça login.", "success")
        return redirect(url_for("auth.login"))
    
    return render_template("register.html")