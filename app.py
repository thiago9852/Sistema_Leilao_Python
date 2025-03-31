
from flask import Flask

# Iniciar o servidor Flask e configurar a aplicação.
app = Flask(__name__)


if __name__ == '__main__':
    app.run(debug=True)