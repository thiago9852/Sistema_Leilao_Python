from flask import Flask
from flask_socketio import SocketIO
from flask_login import LoginManager
from config.config import Config
from routes import auth, auctions
from models import db
from webSocket.auction_events import register_socket_handlers
import eventlet
from database import execute_query
import os

eventlet.monkey_patch()

app = Flask(__name__)

app.secret_key = "segredo_super_secreto"
app.config.from_object(Config)

app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+mysqlconnector://root@127.0.0.1/leilao_db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Inicializando banco de dados
db.init_app(app)

with app.app_context():
    db.create_all()

# Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'auth_bp.login'

@login_manager.user_loader
def load_user(user_id):
    user_data = execute_query(
        "SELECT * FROM user WHERE id = %s", 
        (user_id,), 
        fetch=True
    )
    if user_data:
        from models.user import User
        return User(**user_data[0])
    return None

# Upload de imagem
app.config['UPLOAD_FOLDER'] = os.path.join('static', 'uploads')
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'}

# WebSockets
socketio = SocketIO(app, async_mode='eventlet')

# Registra handlers
register_socket_handlers(socketio)

# Blueprints
app.register_blueprint(auth.auth_bp)
app.register_blueprint(auctions.auction_bp)

if __name__ == '__main__':
    socketio.run(app, debug=True, host="0.0.0.0", port=5000)