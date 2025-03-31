import os

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "minha_chave_secreta")
    #Conexão com o Banco de dados aqui
