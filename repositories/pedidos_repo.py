from models.pedido_compra import PedidoCompra
from models.produto import Produto

class PedidoRepository:
    def buscar_pedidos_por_usuario(self, current_user):
        user_type = current_user['type']

        if user_type == 'cliente':
            pedidos = PedidoCompra.query.filter_by(cliente_id=current_user['sub']).order_by(PedidoCompra.data_pedido.desc()).all()
        elif user_type == 'admin':
            pedidos = PedidoCompra.query.order_by(PedidoCompra.data_pedido.desc()).all()
        else:
            return {"message": "Acesso negado."}, 403

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
                "status": str(pedido.status),  # <<< AQUI!
                "valor_total": f"{pedido.valor_total:.2f}",
                "itens_count": pedido.itens.count(),
                "itens": itens_detalhes
            });
        return pedidos_detalhados
