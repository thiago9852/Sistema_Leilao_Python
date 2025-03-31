# auth.py

from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user, login_required
from models import User
from flask_bcrypt import Bcrypt

# Criação da Blueprint para autenticação
auth_bp = Blueprint('auth_bp', __name__, template_folder='templates', static_folder='static')

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
            return redirect(url_for("main.dashboard"))  # Redireciona para o dashboard
        else:
            flash("Credenciais inválidas.", "danger")

    return render_template("sign/login.html")

@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Logout realizado.", "info")
    return redirect(url_for("main.index"))  # Redireciona para a página inicial
