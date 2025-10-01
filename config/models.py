# models.py
from config.extensions import db
from sqlalchemy import text # Necessário para o ORM referenciar o tipo de dado

# Define a estrutura de dados para o Pet Amigo

class Usuario(db.Model):
    __tablename__ = "usuarios"
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    senha_hash = db.Column(db.Text, nullable=False)
    tipo = db.Column(db.String(20), default='cliente') # 'cliente' ou 'admin'
    created_at = db.Column(db.DateTime, default=text('CURRENT_TIMESTAMP'))
    
    # Adicione este método se quiser usar o ORM para buscar o usuário
    def to_dict(self):
        return {"id": self.id, "email": self.email, "tipo": self.tipo, "nome": self.nome}


class Produto(db.Model):
    # __tablename__ deve ser exatamente o nome da tabela criada no init_db.py
    __tablename__ = "produtos" 
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False, unique=True)
    descricao = db.Column(db.Text)
    # db.Numeric é melhor para dinheiro que db.Float
    preco = db.Column(db.Numeric(10, 2), nullable=False) 
    categoria = db.Column(db.String(50))
    estoque = db.Column(db.Integer, default=0)
    imagem_url = db.Column(db.String(255), default="https://res.cloudinary.com/demo/image/upload/v1690000000/default-product.png")

    def to_dict(self):
        return {
            "id": self.id, 
            "nome": self.nome, 
            # Converte Numeric para string para JSON, garantindo 2 casas decimais
            "preco": f"{self.preco:.2f}", 
            "descricao": self.descricao,
            "estoque": self.estoque,
            "categoria": self.categoria,
            "imagem_url": self.imagem_url
        }

class PedidoCompra(db.Model):
    __tablename__ = "pedidos_compra"
    id = db.Column(db.Integer, primary_key=True)
    cliente_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    data_pedido = db.Column(db.DateTime, default=text('CURRENT_TIMESTAMP'))
    status = db.Column(db.String(20), default='pendente') # 'pendente', 'processando', 'concluido'
    valor_total = db.Column(db.Numeric(10, 2), nullable=False)
    endereco_entrega = db.Column(db.Text)
    
    # Relação para buscar os itens deste pedido
    itens = db.relationship('ItemPedido', backref='pedido', lazy='dynamic') 

    def to_dict(self):
        return {
            "id": self.id,
            "cliente_id": self.cliente_id,
            "data_pedido": self.data_pedido.isoformat(),
            "status": self.status,
            "valor_total": f"{self.valor_total:.2f}",
            "itens_count": self.itens.count()
        }

class ItemPedido(db.Model):
    __tablename__ = "itens_pedido"
    id = db.Column(db.Integer, primary_key=True)
    pedido_id = db.Column(db.Integer, db.ForeignKey('pedidos_compra.id'), nullable=False)
    produto_id = db.Column(db.Integer, db.ForeignKey('produtos.id'), nullable=False)
    quantidade = db.Column(db.Integer, nullable=False)
    preco_unitario = db.Column(db.Numeric(10, 2), nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "pedido_id": self.pedido_id,
            "produto_id": self.produto_id,
            "quantidade": self.quantidade,
            "preco_unitario": self.preco_unitario
        }