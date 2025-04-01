from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

# Configuração do banco de dados MySQL
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+mysqlconnector://flask_user:SenhaForte@123@localhost/leilao_db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

# Modelo para Leilão
class Leilao(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    item = db.Column(db.String(100), nullable=False)
    descricao = db.Column(db.Text, nullable=True)
    preco_inicial = db.Column(db.Float, nullable=False)
    lance_minimo = db.Column(db.Float, nullable=False)  # NOVO
    lance_maximo = db.Column(db.Float, nullable=False)  # NOVO
    data_inicio = db.Column(db.DateTime, default=datetime.utcnow)
    data_fim = db.Column(db.DateTime, nullable=False)
    lances = db.relationship("Lance", backref="leilao", lazy=True)

# Modelo para Lance
class Lance(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    usuario = db.Column(db.String(50), nullable=False)
    valor = db.Column(db.Float, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    leilao_id = db.Column(db.Integer, db.ForeignKey("leilao.id"), nullable=False)

# Criar tabelas no banco de dados
with app.app_context():
    db.create_all()
