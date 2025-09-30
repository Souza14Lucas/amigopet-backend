# app.py
from flask import Flask, jsonify
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

# CONFIGURAÇÃO DO POSTGRESQL (Mantida)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql+psycopg2://{user}:{password}@{host}:{port}/{db}".format(
    user=os.getenv('DB_USER'),
    password=os.getenv('DB_PASSWORD'),
    host=os.getenv('DB_HOST'),
    port=os.getenv('DB_PORT'), # 5432
    db=os.getenv('DB_NAME')
)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

# NOVO: Adiciona a URL do Frontend Admin (Static Site) para permissão CORS
# O Render precisa disso para aceitar requisições do seu painel Admin
FRONTEND_ADMIN_URL = os.getenv('FRONTEND_ADMIN_URL', '*')

# NOVO: Associa a instância do DB ao aplicativo
print("DB URI:", app.config['SQLALCHEMY_DATABASE_URI'])
db.init_app(app)

# Configuração do CORS: Permite requisições de origens específicas
CORS(app, resources={r"/api/*": {"origins": [FRONTEND_ADMIN_URL, "http://localhost:5000", "http://127.0.0.1:5000"]}})

# Registra os Blueprints
app.register_blueprint(auth_bp, url_prefix='/api/auth')
app.register_blueprint(produtos_bp, url_prefix='/api/produtos')
app.register_blueprint(pedidos_bp, url_prefix='/api/pedidos') # NOVO


# 5. Rota de Teste (Exemplo de API)
@app.route('/', methods=['GET'])
def index():
    """Rota de teste inicial."""
    return jsonify({
        "message": "Servidor Amigo Pet (Python/Flask) rodando!",
        "status": "online"
    }), 200


# 6. Inicialização do Servidor
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    # debug=True: recarrega o servidor automaticamente ao salvar mudanças no código
    app.run(debug=True, host='0.0.0.0', port=port)