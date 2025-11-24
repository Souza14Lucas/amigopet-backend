from flask import Flask, jsonify, request
from dotenv import load_dotenv
import os
from flask_cors import CORS 
from config.extensions import db 
from routes.auth_routes import auth_bp 
from routes.produtos_route import produtos_bp
from routes.pedidos_routes import pedidos_bp

load_dotenv()
app = Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql+psycopg2://{user}:{password}@{host}:{port}/{db}".format(
    user=os.getenv('DB_USER'),
    password=os.getenv('DB_PASSWORD'),
    host=os.getenv('DB_HOST'),
    port=os.getenv('DB_PORT'),
    db=os.getenv('DB_NAME')
)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.config['SECRET_KEY'] = os.getenv('SECRET_KEY') 

FRONTEND_ADMIN_URL = os.getenv('FRONTEND_ADMIN_URL', 'https://amigopet-admin-crud.onrender.com')
FRONTEND_API_URL = os.getenv('RENDER_EXTERNAL_URL') 

ALLOWED_ORIGINS = [
    "http://localhost:5000",
    "http://localhost:3000",
    "http://127.0.0.1:5000",
    FRONTEND_ADMIN_URL
]

if FRONTEND_API_URL:
    ALLOWED_ORIGINS.append(FRONTEND_API_URL)

# Configuração de CORS
CORS(app, resources={r"/api/*": {
    "origins": [
        "https://amigopet-admin-crud.onrender.com",
        "http://localhost:5000",
        "http://localhost:3000",
    ],
    "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    "allow_headers": ["Authorization", "Content-Type"],
    "supports_credentials": True
}})

@app.before_request
def handle_preflight():
    if request.method == "OPTIONS":
        return "", 200

db.init_app(app)

# Blueprints
app.register_blueprint(auth_bp, url_prefix='/api/auth')
app.register_blueprint(produtos_bp, url_prefix='/api/produtos')
app.register_blueprint(pedidos_bp, url_prefix='/api/pedidos')

# Rota de teste - flask inicialização
@app.route('/', methods=['GET'])
def index():
    return jsonify({
        "message": "Servidor Pet Amigo (Python/Flask) rodando!",
        "status": "online"
    }), 200

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
