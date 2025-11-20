from models.produto import Produto
from repositories.produtos_repo import ProdutoRepository
from config.extensions import db

class ProdutoService:
    def __init__(self):
        self.repo = ProdutoRepository()

    def criar_produto(self, data, current_user):
        if current_user['type'] != 'admin':
            return {"message": "Permissão negada. Apenas administradores podem criar produtos."}, 403

        nome = data.get('nome')
        preco = data.get('preco')

        if not all([nome, preco]):
            return {"message": "Campos 'nome' e 'preco' são obrigatórios."}, 400

        try:
            novo_produto = Produto(
                nome=nome,
                descricao=data.get('descricao'),
                preco=preco,
                categoria=data.get('categoria'),
                estoque=data.get('estoque', 0),
                imagem_url=data.get('imagem_url'),
                especie=data.get('especie'),
            )

            produto_criado = self.repo.criar(novo_produto)
            return {
                "message": f"Produto '{nome}' criado com sucesso por {current_user['sub']}",
                "produto_id": produto_criado.id
            }, 201

        except Exception as e:
            db.session.rollback()
            print(f"Erro ao criar produto: {e}")
            return {"message": "Ocorreu um erro ao criar o produto."}, 500


    def listar_produtos(self):
        try:
            produtos = self.repo.listar_todos()
            return [p.to_dict() for p in produtos], 200
        except Exception as e:
            print(f"Erro ao listar produtos: {e}")
            return {"message": "Erro interno ao buscar produtos."}, 500


    def buscar_produto_por_id(self, produto_id):
        produto = self.repo.buscar_por_id(produto_id)
        if not produto:
            return {"message": "Produto não encontrado"}, 404
        return produto.to_dict(), 200


    def atualizar_produto(self, produto_id, data, current_user):
        if current_user['type'] != 'admin':
            return {"message": "Permissão negada. Apenas administradores podem atualizar produtos."}, 403

        produto = self.repo.buscar_por_id(produto_id)
        if not produto:
            return {"message": "Produto não encontrado."}, 404

        produto.nome = data.get('nome', produto.nome)
        produto.preco = data.get('preco', produto.preco)
        produto.estoque = data.get('estoque', produto.estoque)
        produto.categoria = data.get('categoria', produto.categoria)
        produto.descricao = data.get('descricao', produto.descricao)
        produto.imagem_url = data.get('imagem_url', produto.imagem_url)
        produto.especie = data.get('especie', produto.especie)

        self.repo.atualizar(produto)
        return {"message": "Produto atualizado com sucesso!", "produto": produto.to_dict()}, 200


    def deletar_produto(self, produto_id, current_user):
        if current_user['type'] != 'admin':
            return {"message": "Permissão negada. Apenas administradores podem deletar produtos."}, 403

        produto = self.repo.buscar_por_id(produto_id)
        if not produto:
            return {"message": "Produto não encontrado."}, 404

        self.repo.deletar(produto)
        return {"message": f"Produto '{produto.nome}' deletado com sucesso!"}, 200
