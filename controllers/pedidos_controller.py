from services.pedidos_services import PedidoService

class PedidoController:
    def __init__(self):
        self.service = PedidoService()

    def criar_pedido(self, data, current_user):
        
        try:
            return self.service.criar_pedido(data, current_user)
        except Exception as e:
            print(f"Erro no controller: {e}")
            return {"error:" "Erro interno ao processar o pedido."}, 500
        
    def buscar_pedidos(self, current_user):
        try:
            return self.service.buscar_pedidos(current_user)
        except Exception as e:
            print(f"Erro no controller: {e}")
            return {"error": "Erro interno ao buscar pedidos."}, 500