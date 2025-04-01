# Código para criar a tabela USER no banco de dados
# Modelo para Usuário
class User(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    senha = db.Column(db.String(255), nullable=False)  # Armazene hashes de senha, não texto puro
    data_criacao = db.Column(db.DateTime, default=datetime.utcnow)
