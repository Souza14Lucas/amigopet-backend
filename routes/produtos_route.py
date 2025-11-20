from flask import Blueprint, jsonify, request
from config.extensions import db 
from utils.security import token_required
from flask import Blueprint, jsonify, request
from utils.security import token_required
from controllers.produtos_controller import ProdutoController

produtos_bp = Blueprint('produtos', __name__)
controller = ProdutoController()

# só admin
@produtos_bp.route('/criar-produto', methods=['POST'])
@token_required
def criar_produto(current_user):
    data = request.get_json()
    response, status = controller.criar_produto(data, current_user)
    return jsonify(response), status


@produtos_bp.route('/listar-produtos', methods=['GET'])
def listar_produtos():
    response, status = controller.listar_produtos()
    return jsonify(response), status


@produtos_bp.route('/<int:produto_id>', methods=['GET'])
def buscar_produto(produto_id):
    response, status = controller.buscar_produto_por_id(produto_id)
    return jsonify(response), status

# só admin
@produtos_bp.route('/<int:produto_id>', methods=['PUT'])
@token_required
def atualizar_produto(current_user, produto_id):
    data = request.get_json()
    response, status = controller.atualizar_produto(produto_id, data, current_user)
    return jsonify(response), status

# só admin
@produtos_bp.route('/<int:produto_id>', methods=['DELETE'])
@token_required
def deletar_produto(current_user, produto_id):
    response, status = controller.deletar_produto(produto_id, current_user)
    return jsonify(response), status
