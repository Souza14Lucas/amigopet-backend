from config.extensions import db
from models.pedido_compra import PedidoCompra
from models.item_pedido import ItemPedido
from models.produto import Produto
from repositories.pedidos_repo import PedidoRepository

class PedidoService:
    def __init__(self):
        self.repo = PedidoRepository()

    def criar_pedido(self, data, current_user):
        itens = data.get('itens', [])
        endereco_entrega = data.get('endereco')
        cliente_id = current_user['sub']

        if not itens or not endereco_entrega:
            return {"error": "Itens e endereço são obrigatórios."}, 400

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
                return {"error": "Estoque insuficiente ou produto não encontrado."}, 400

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

        return {
            "message": "Pedido criado com sucesso!",
            "pedido_id": pedido.id,
            "valor_total": float(valor_total)
        }, 201

    def buscar_pedidos(self, current_user):
        pedidos = self.repo.buscar_pedidos_por_usuario(current_user)
        return pedidos, 200