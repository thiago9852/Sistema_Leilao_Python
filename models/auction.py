from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

# Configuração do banco de dados MySQL
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+mysqlconnector://root@127.0.0.1/leilao_db"
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
    contador_lances = db.Column(db.Integer, default=0) 
    lances = db.relationship("Lance", backref="leilao", lazy=True)

# Criar tabelas no banco de dados
with app.app_context():
    db.create_all()