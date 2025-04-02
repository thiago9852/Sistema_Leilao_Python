from datetime import datetime
from models import db  # Importando a instância compartilhada de db

class Lance(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    valor = db.Column(db.Float, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    leilao_id = db.Column(db.Integer, db.ForeignKey("leilao.id"), nullable=False)
    contador_lance = db.Column(db.Integer, default=1)  # Contador de lances por usuário
    usuario_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)