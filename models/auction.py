from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

# Configuração do banco de dados MySQL
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+mysqlconnector://root:root@localhost/leilao_db"
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

# Modelo para Lance
class Lance(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    usuario = db.Column(db.String(50), nullable=False)
    valor = db.Column(db.Float, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    leilao_id = db.Column(db.Integer, db.ForeignKey("leilao.id"), nullable=False)
    contador_usuarios = db.Column(db.Integer, default=1)  # Contador de lances por usuário

# Criar tabelas no banco de dados
with app.app_context():
    db.create_all()

# Criar um leilão
@app.route("/leilao", methods=["POST"])
def criar_leilao():
    data = request.json
    novo_leilao = Leilao(
        item=data["item"],
        descricao=data.get("descricao"),
        preco_inicial=data["preco_inicial"],
        lance_minimo=data["lance_minimo"],  # NOVO
        lance_maximo=data["lance_maximo"],  # NOVO
        data_fim=datetime.strptime(data["data_fim"], "%Y-%m-%d %H:%M:%S")
    )
    db.session.add(novo_leilao)
    db.session.commit()
    return jsonify({"mensagem": "Leilão criado com sucesso!", "id": novo_leilao.id})

# Listar leilões
@app.route("/leiloes", methods=["GET"])
def listar_leiloes():
    leiloes = Leilao.query.all()
    resultado = [
        {
            "id": leilao.id,
            "item": leilao.item,
            "descricao": leilao.descricao,
            "preco_inicial": leilao.preco_inicial,
            "lance_minimo": leilao.lance_minimo,  # NOVO
            "lance_maximo": leilao.lance_maximo,  # NOVO
            "data_inicio": leilao.data_inicio.strftime("%Y-%m-%d %H:%M:%S"),
            "data_fim": leilao.data_fim.strftime("%Y-%m-%d %H:%M:%S")
        }
        for leilao in leiloes
    ]
    return jsonify(resultado)

# Dar um lance em um leilão
@app.route("/lance", methods=["POST"])
def dar_lance():
    data = request.json
    leilao = Leilao.query.get(data["leilao_id"])

    if not leilao:
        return jsonify({"erro": "Leilão não encontrado"}), 404

    if not (leilao.lance_minimo <= data["valor"] <= leilao.lance_maximo):
        return jsonify({"erro": f"O lance deve estar entre {leilao.lance_minimo} e {leilao.lance_maximo}"}), 400

    maior_lance = Lance.query.filter_by(leilao_id=leilao.id).order_by(Lance.valor.desc()).first()
    if maior_lance and data["valor"] <= maior_lance.valor:
        return jsonify({"erro": "O lance deve ser maior que o maior lance atual"}), 400

    novo_lance = Lance(
        usuario=data["usuario"],
        valor=data["valor"],
        leilao_id=data["leilao_id"]
    )
    db.session.add(novo_lance)
    db.session.commit()
    return jsonify({"mensagem": "Lance realizado com sucesso!", "id": novo_lance.id})

# Listar lances de um leilão
@app.route("/lances/<int:leilao_id>", methods=["GET"])
def listar_lances(leilao_id):
    lances = Lance.query.filter_by(leilao_id=leilao_id).order_by(Lance.timestamp.desc()).all()
    resultado = [
        {
            "id": lance.id,
            "usuario": lance.usuario,
            "valor": lance.valor,
            "timestamp": lance.timestamp.strftime("%Y-%m-%d %H:%M:%S")
        }
        for lance in lances
    ]
    return jsonify(resultado)

if __name__ == "__main__":
    app.run(debug=True)
