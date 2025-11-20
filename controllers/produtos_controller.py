from services.produto_service import ProdutoService

class ProdutoController:
    def __init__(self):
        self.service = ProdutoService()

    def criar_produto(self, data, current_user):
        return self.service.criar_produto(data, current_user)

    def listar_produtos(self):
        return self.service.listar_produtos()

    def buscar_produto_por_id(self, produto_id):
        return self.service.buscar_produto_por_id(produto_id)

    def atualizar_produto(self, produto_id, data, current_user):
        return self.service.atualizar_produto(produto_id, data, current_user)

    def deletar_produto(self, produto_id, current_user):
        return self.service.deletar_produto(produto_id, current_user)
