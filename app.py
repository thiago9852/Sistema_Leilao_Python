from flask import Flask
from flask_socketio import SocketIO
from config.config import Config
from routes import auth, auction
from webSocket.auction import register_socket_handlers
import eventlet

eventlet.monkey_patch()

app = Flask(__name__)

app.secret_key("segredo_super_secreto")
app.config.from_object(Config)
    
# WebSockets
socketio = SocketIO(app, 
    async_mode='eventlet',
    message_queue=app.config['REDIS_URL']
)

# Registra handlers
register_socket_handlers(socketio)

# Blueprints
app.register_blueprint(auth.auth_bp)
app.register_blueprint(auction.auction_bp)

if __name__ == '__main__':
    socketio.run(app, debug=True)