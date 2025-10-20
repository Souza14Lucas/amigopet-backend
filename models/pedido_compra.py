from config.extensions import db
from sqlalchemy import text

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