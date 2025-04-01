# filepath: c:\Users\thiag\OneDrive\Área de Trabalho\Leilao BSI\models\lance.py
from models import db
from datetime import datetime

class Lance(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    usuario = db.Column(db.String(50), nullable=False)
    valor = db.Column(db.Float, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    leilao_id = db.Column(db.Integer, db.ForeignKey("leilao.id"), nullable=False)
    contador_usuarios = db.Column(db.Integer, default=1)  # Contador de lances por usuário