import os

class Config:
    SECRET_KEY = os.getenv("app.config[""SQLALCHEMY_DATABASE_URI"] = "mysql+mysqlconnector://flask_user:SenhaForte@123@localhost/leilao_db")
    #Conexão com o Banco de dados aqui
