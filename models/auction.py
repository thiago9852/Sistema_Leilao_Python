from models import db
from .lance import Lance
from .user import User
from datetime import datetime
from sqlalchemy import func
from sqlalchemy.ext.hybrid import hybrid_property

class Leilao(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    item = db.Column(db.String(100), nullable=False)
    descricao = db.Column(db.String(255), nullable=False)
    sobre = db.Column(db.Text, nullable=True)
    lance_inicial = db.Column(db.Float, nullable=False)
    lance_minimo = db.Column(db.Float, nullable=False, default=0) 
    lance_maximo = db.Column(db.Float, nullable=True)
    data_inicio = db.Column(db.DateTime, nullable=False)
    data_fim = db.Column(db.DateTime, nullable=False)
    categoria = db.Column(db.String(50), nullable=False)
    visualizacoes = db.Column(db.Integer, default=0)
    status = db.Column(db.String(15), default="ativo", nullable=False)
    imagem_url = db.Column(db.String(255), nullable=False)
    vencedor_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    criador_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    # Relacionamentos
    lances = db.relationship("Lance", backref="leilao", lazy="dynamic", cascade="all, delete-orphan")


    @property
    def maior_lance(self):
        maior = db.session.query(func.max(Lance.valor)).filter_by(leilao_id=self.id).scalar()
        return maior if maior is not None else self.lance_inicial
    
    @property
    def maior_lance_info(self):
        return db.session.query(
            Lance.valor,
            User.nome,
            User.id
        ).join(User).filter(
            Lance.leilao_id == self.id
        ).order_by(
            Lance.valor.desc()
        ).first()
        
    # Propriedade para contar lances
    @hybrid_property
    def total_lances(self):
        return self.lances.count()

    def __repr__(self):
        return f'<Leilao {self.id} - {self.item}>'

    # Métodos de negócio
    def esta_ativo(self): # is_ativo
        return self.status == "ativo" and datetime.utcnow() < self.data_fim

    def encerrar(self, vencedor=None): # encerrar
        self.status = "finalizado"
        if vencedor:
            self.vencedor = vencedor
        db.session.commit()

    def atualizar_maior_lance(self):
        self._maior_lance = self.maior_lance
        db.session.commit()