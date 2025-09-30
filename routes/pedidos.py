# routes/pedidos.py
from flask import Blueprint, jsonify, request
from config.extensions import db
from utils.security import token_required
from config.models import Produto, PedidoCompra, ItemPedido  # Certifique-se de que esses modelos existem
from sqlalchemy.exc import IntegrityError

pedidos_bp = Blueprint('pedidos', __name__)

# -------------------------------------------------------------
# ROTA 1: Solicitar Pedido (POST /api/pedidos)
# -------------------------------------------------------------
@pedidos_bp.route('/', methods=['POST'])
@token_required
def solicitar_pedido(current_user):
    data = request.get_json()
    itens = data.get('itens', [])
    endereco_entrega = data.get('endereco')
    cliente_id = current_user['sub']

    if not itens or not endereco_entrega:
        return jsonify({"error": "Itens e endereço são obrigatórios."}), 400

    try:
        pedido = PedidoCompra(cliente_id=cliente_id, endereco_entrega=endereco_entrega, valor_total=0)
        db.session.add(pedido)
        db.session.flush()

        valor_total = 0
        itens_para_adicionar = []

        for item in itens:
            produto = Produto.query.get(item.get('produto_id'))
            quantidade = item.get('quantidade')

            if not produto or produto.estoque < quantidade:
                db.session.rollback()
                return jsonify({"error": f"Estoque insuficiente ou produto não encontrado."}), 400

            preco_unitario = produto.preco
            subtotal = preco_unitario * quantidade
            valor_total += subtotal

            itens_para_adicionar.append(
                ItemPedido(
                    pedido_id=pedido.id,
                    produto_id=produto.id,
                    quantidade=quantidade,
                    preco_unitario=preco_unitario
                )
            )

            produto.estoque -= quantidade

        pedido.valor_total = valor_total
        db.session.add_all(itens_para_adicionar)
        db.session.commit()

        return jsonify({"message": "Pedido criado com sucesso!", "pedido_id": pedido.id, "valor_total": float(valor_total)}), 201

    except Exception as e:
        db.session.rollback()
        print(f"Erro ao solicitar pedido: {e}")
        return jsonify({"error": "Ocorreu um erro interno ao processar o pedido."}), 500


# -------------------------------------------------------------
# ROTA 2: Buscar Pedidos (GET /api/pedidos)
# -------------------------------------------------------------
@pedidos_bp.route('/', methods=['GET'])
@token_required
def buscar_pedidos(current_user):
    user_type = current_user['type']
    
    if user_type == 'cliente':
        # Clientes veem apenas seus pedidos
        pedidos = PedidoCompra.query.filter_by(cliente_id=current_user['sub']).order_by(PedidoCompra.data_pedido.desc()).all()
    elif user_type == 'admin':
        # Administradores veem todos os pedidos
        pedidos = PedidoCompra.query.order_by(PedidoCompra.data_pedido.desc()).all()
    else:
        return jsonify({"message": "Acesso negado."}), 403

    # Cria uma lista detalhada dos pedidos
    pedidos_detalhados = []
    for pedido in pedidos:
        itens_detalhes = []
        for item in pedido.itens:
            produto = Produto.query.get(item.produto_id)
            itens_detalhes.append({
                "produto_id": item.produto_id,
                "nome_produto": produto.nome if produto else "Produto não encontrado",
                "quantidade": item.quantidade,
                "preco_unitario": f"{item.preco_unitario:.2f}",
                "subtotal": f"{item.preco_unitario * item.quantidade:.2f}"
            })
        pedidos_detalhados.append({
            "pedido_id": pedido.id,
            "cliente_id": pedido.cliente_id,
            "data_pedido": pedido.data_pedido.isoformat(),
            "status": pedido.status,
            "valor_total": f"{pedido.valor_total:.2f}",
            "itens_count": pedido.itens.count(),
            "itens": itens_detalhes
        })

    return jsonify(pedidos_detalhados), 200
