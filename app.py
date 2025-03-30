from flask import Flask, render_template, redirect, url_for, request, flash
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from flask_bcrypt import Bcrypt

app = Flask(__name__)
app.secret_key = "chave-secreta"

bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = "login"

# Simulação de banco de dados para testar
users = []

class User(UserMixin):
    def __init__(self, email, nome, senha):
        self.id = email
        self.nome = nome
        self.email = email
        self.senha = senha

@login_manager.user_loader
def load_user(email):
    user = next((user for user in users if user['email'] == email), None)
    if user:
        return User(user['email'], user['nome'], user['senha'])
    return None

# ROTAS PARA O FLASK
@app.route("/")
@app.route("/index")
def index():
    return render_template("index.html")

@app.route("/dashboard")
@login_required
def dashboard():
    return render_template("dashboard.html")

@app.route("/leiloes")
def leiloes():
    return render_template("/leilao/index.html")

@app.route("/leiloes/show")
def leiloes_show():
    return render_template("/leilao/show.html")

@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Logout realizado.", "info")
    return redirect(url_for("index"))


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        senha = request.form["senha"]

        # Autenticação do usuário
        user = next((user for user in users if user['email'] == email), None)
        
        if user and bcrypt.check_password_hash(user['senha'], senha):
            user_obj = User(user['email'], user['nome'], user['senha'])
            login_user(user_obj)
            flash("Login bem-sucedido!", "success")
            return redirect(url_for("dashboard"))
        else:
            flash("Credenciais inválidas.", "danger")

    return render_template("sign/login.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        nome = request.form["nome"]
        email = request.form["email"]
        senha = request.form["senha"]

        # Verificar se o email já está cadastrado
        if any(user['email'] == email for user in users):
            flash("Email já registrado!", "warning")
        else:
            # Criptografar a senha
            senha_hash = bcrypt.generate_password_hash(senha).decode("utf-8")
            
            # Armazenar o novo usuário
            users.append({"nome": nome, "email": email, "senha": senha_hash})

            flash("Usuário registrado com sucesso!", "success")
            return redirect(url_for("login"))

    return render_template("sign/register.html")


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
