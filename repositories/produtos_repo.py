from config.extensions import db
from models.produto import Produto

class ProdutoRepository:

    def criar(self, produto):
        db.session.add(produto)
        db.session.commit()
        return produto

    def listar_todos(self):
        return Produto.query.filter(Produto.estoque > 0).order_by(Produto.id.asc()).all()

    def buscar_por_id(self, produto_id):
        return Produto.query.get(produto_id)

    def atualizar(self, produto):
        db.session.commit()
        return produto

    def deletar(self, produto):
        db.session.delete(produto)
        db.session.commit()
