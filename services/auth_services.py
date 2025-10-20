# services/auth_service.py
from config.extensions import db
from models.usuario import Usuario
from utils.security import hash_password, create_jwt_token, check_password
from sqlalchemy.exc import IntegrityError

class AuthService:

    @staticmethod
    def registrar(data):
        nome = data.get('nome')
        email = data.get('email')
        senha = data.get('senha')
        tipo = data.get('tipo', 'cliente')

        if not all([nome, email, senha]):
            raise ValueError("Todos os campos são obrigatórios")

        senha_hash = hash_password(senha)

        try:
            novo_usuario = Usuario(
                nome=nome,
                email=email,
                senha_hash=senha_hash,
                tipo=tipo
            )
            db.session.add(novo_usuario)
            db.session.commit()

            token = create_jwt_token(novo_usuario.id, novo_usuario.tipo)
            return {
                "message": "Usuário registrado com sucesso!",
                "token": token,
                "user_id": novo_usuario.id,
                "user_type": novo_usuario.tipo
            }

        except IntegrityError:
            db.session.rollback()
            raise ValueError("O email fornecido já está em uso.")
    
    @staticmethod
    def login_usuario(data):
        email = data.get('email')
        senha = data.get('senha')

        if not all([email, senha]):
            raise ValueError("Email e senha são obrigatórios")

        usuario = Usuario.query.filter_by(email=email).first()

        if not usuario or not check_password(senha, usuario.senha_hash):
         raise ValueError("Email ou senha inválidos")

        token = create_jwt_token(usuario.id, usuario.tipo)

        return {
            "token": token,
            "message": "Login realizado com sucesso!",
            "user_id": usuario.id,
            "user_type": usuario.tipo,
            "user_name": usuario.nome
        }
