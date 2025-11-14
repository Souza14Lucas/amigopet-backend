from flask import Blueprint, request
from controllers.auth_controller import registrar_usuario, login_usuario

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/registro', methods=['POST'])
def register_user():
    data = request.get_json()
    return registrar_usuario(data)


@auth_bp.route('/login', methods=['POST'])
def login_user():
    data = request.get_json()
    return login_usuario(data)
