from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
        
from .user import User
from .auction import Leilao
from .lance import Lance