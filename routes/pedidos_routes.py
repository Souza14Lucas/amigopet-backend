from flask import Blueprint, jsonify, request
from config.extensions import db
from controllers.pedidos_controller import PedidoController
from utils.security import token_required
from sqlalchemy.exc import IntegrityError

pedidos_bp = Blueprint('pedidos', __name__)
controller = PedidoController()


@pedidos_bp.route('/criar-pedido', methods=['POST'])
@token_required
def solicitar_pedido(current_user):
    data = request.get_json()
    response, status = controller.criar_pedido(data, current_user)
    return jsonify(response), status


@pedidos_bp.route('/buscar-pedidos', methods=['GET'])
@token_required
def buscar_pedidos(current_user):
    response, status = controller.buscar_pedidos(current_user)
    return jsonify(response), status