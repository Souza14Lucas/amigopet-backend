import bcrypt
import jwt
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv
from flask import request, jsonify
from functools import wraps

load_dotenv()
SECRET_KEY = os.getenv('SECRET_KEY') 

# --- 1. Criptografia de senha ---
def hash_password(password):
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8')

def check_password(password, hashed_password):
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))

# --- 2. JWT ---
def create_jwt_token(user_id, user_type):
    payload = {
        'exp': datetime.utcnow() + timedelta(days=1),
        'iat': datetime.utcnow(),
        'sub': str(user_id),   # <-- alteração
        'type': user_type
    }
    return jwt.encode(payload, SECRET_KEY, algorithm='HS256')

def decode_jwt_token(token):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        return payload
    except jwt.ExpiredSignatureError:
        return {'error': 'Token expirado'}
    except jwt.InvalidTokenError:
        return {'error': 'Token inválido'}

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            try:
                token = auth_header.split()[1]
            except IndexError:
                return jsonify({'message': 'Token inválido ou faltando prefixo Bearer'}), 401

        if not token:
            return jsonify({'message': 'Token de acesso é obrigatório'}), 401

        try:
            current_user = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
            print("Payload decodificado:", current_user)
        except jwt.ExpiredSignatureError:
            return jsonify({'message': 'Token expirado'}), 401
        except jwt.InvalidTokenError as e:
            print("Erro JWT:", e)
            return jsonify({'message': 'Token inválido'}), 401

        return f(current_user, *args, **kwargs)

    return decorated
