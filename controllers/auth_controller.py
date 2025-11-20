from services.auth_services import AuthService
from flask import jsonify

def registrar_usuario(data):
    try:
        result = AuthService.registrar(data)
        return jsonify(result), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": f"Erro interno: {str(e)}"}), 500


def login_usuario(data):
    try:
        result = AuthService.login_usuario(data) 
        return jsonify(result), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"Error": "Erro interno"}), 500