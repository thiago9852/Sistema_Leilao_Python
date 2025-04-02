from datetime import datetime
from models import db  # Importando a instância compartilhada de db
from flask_login import UserMixin


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    senha = db.Column(db.String(255), nullable=False)
    data_criacao = db.Column(db.DateTime, default=datetime.utcnow)


    leiloes_criados = db.relationship(
        'Leilao',
        foreign_keys='Leilao.criador_id',
        backref='criador',
        lazy=True
    )
    
    leiloes_vencidos = db.relationship(
        'Leilao',
        foreign_keys='Leilao.vencedor_id',
        backref='vencedor',
        lazy=True
    )
    
    lances = db.relationship('Lance', backref='usuario', lazy=True)