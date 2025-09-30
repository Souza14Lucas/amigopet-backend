from flask import Flask, jsonify, request
from dotenv import load_dotenv
import os
from flask_cors import CORS 

# Importa a lógica de conexão com o DB
from config.extensions import db 

from routes.auth import auth_bp 
from routes.produtos import produtos_bp
from routes.pedidos import pedidos_bp

# 1. Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

# 2. Inicializa o aplicativo Flask
app = Flask(__name__)

# CONFIGURAÇÃO DO POSTGRESQL
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql+psycopg2://{user}:{password}@{host}:{port}/{db}".format(
    user=os.getenv('DB_USER'),
    password=os.getenv('DB_PASSWORD'),
    host=os.getenv('DB_HOST'),
    port=os.getenv('DB_PORT'),
    db=os.getenv('DB_NAME')
)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.config['SECRET_KEY'] = os.getenv('SECRET_KEY') 

# URLs permitidas (frontend admin + localhost)
FRONTEND_ADMIN_URL = os.getenv('FRONTEND_ADMIN_URL', 'https://amigopet-admin-crud.onrender.com')
FRONTEND_API_URL = os.getenv('RENDER_EXTERNAL_URL') 

ALLOWED_ORIGINS = [
    "http://localhost:5000",
    "http://127.0.0.1:5000",
    FRONTEND_ADMIN_URL
]

if FRONTEND_API_URL:
    ALLOWED_ORIGINS.append(FRONTEND_API_URL)

# Configuração do CORS
CORS(app, resources={r"/api/*": {
    "origins": [
        "https://amigopet-admin-crud.onrender.com",
        "http://localhost:5000"  # se você testar local
    ],
    "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    "allow_headers": ["Authorization", "Content-Type"],
    "supports_credentials": True
}})

# 🔑 Corrige o problema do preflight (OPTIONS)
@app.before_request
def handle_preflight():
    if request.method == "OPTIONS":
        # Retorna resposta vazia com 200 e CORS headers
        return "", 200

# Associa DB
db.init_app(app)

# Blueprints
app.register_blueprint(auth_bp, url_prefix='/api/auth')
app.register_blueprint(produtos_bp, url_prefix='/api/produtos')
app.register_blueprint(pedidos_bp, url_prefix='/api/pedidos')

# Rota de teste
@app.route('/', methods=['GET'])
def index():
    return jsonify({
        "message": "Servidor Pet Amigo (Python/Flask) rodando!",
        "status": "online"
    }), 200

# Inicialização
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
