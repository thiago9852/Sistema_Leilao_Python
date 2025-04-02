from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# Importação dos modelos
from .user import User
from .auction import Leilao
from .lance import Lance

def init_db(app):
    db.init_app(app)
    with app.app_context():
        db.create_all()