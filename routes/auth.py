from flask import Blueprint, request, jsonify
from config.extensions import db
from config.models import Usuario
from sqlalchemy.exc import IntegrityError
from utils.security import hash_password, check_password, create_jwt_token

auth_bp = Blueprint('auth', __name__)

# ---------------------------
# Rota de Registro
# ---------------------------
@auth_bp.route('/registro', methods=['POST'])
def register_user():
    data = request.get_json()
    nome = data.get('nome')
    email = data.get('email')
    senha = data.get('senha')
    user_type = data.get('tipo', 'cliente')  # default cliente

    if not all([nome, email, senha]):
        return jsonify({"error": "Todos os campos são obrigatórios"}), 400

    senha_hash = hash_password(senha)
    
    try:
        novo_usuario = Usuario(
            nome=nome,
            email=email,
            senha_hash=senha_hash,
            tipo=user_type
        )
        db.session.add(novo_usuario)
        db.session.commit()

        token = create_jwt_token(novo_usuario.id, novo_usuario.tipo)

        return jsonify({
            "message": "Usuário registrado com sucesso!",
            "token": token,
            "user_id": novo_usuario.id,
            "user_type": novo_usuario.tipo
        }), 201

    except IntegrityError:
        db.session.rollback()
        return jsonify({"error": "O email fornecido já está em uso."}), 409
    
    except Exception as e:
        db.session.rollback()
        print(f"Erro ao registrar usuário: {e}")
        return jsonify({"error": "Ocorreu um erro interno no servidor."}), 500


# ---------------------------
# Rota de Login
# ---------------------------
@auth_bp.route('/login', methods=['POST'])
def login_user():
    data = request.get_json()
    email = data.get('email')
    senha = data.get('senha')

    user = None

    if not all([email, senha]):
        return jsonify({"error": "Email e senha são obrigatórios"}), 400

    try:
        usuario = Usuario.query.filter_by(email=email).first()
        if not usuario or not check_password(senha, usuario.senha_hash):
            return jsonify({"error": "Email ou senha inválidos"}), 401

        token = create_jwt_token(usuario.id, usuario.tipo)

        return jsonify({
            "message": "Login realizado com sucesso!",
            "token": token,
            "user_id": usuario.id,
            "user_type": usuario.tipo
        }), 200

    except Exception as e:
        db.session.rollback()
        print(f"Erro ao logar usuário: {e}")
        print("-" * 50)
        print(f"ERRO CRÍTICO NO LOGIN: {e}")
        print("-" * 50)
        return jsonify({"error": "Ocorreu um erro interno no servidor."}), 500