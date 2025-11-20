from config.extensions import db
from sqlalchemy import text

class Produto(db.Model):
    __tablename__ = "produtos" 
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False, unique=True)
    descricao = db.Column(db.Text)
    preco = db.Column(db.Numeric(10, 2), nullable=False) 
    categoria = db.Column(db.String(50))
    estoque = db.Column(db.Integer, default=0)
    imagem_url = db.Column(db.String(255), default="https://res.cloudinary.com/demo/image/upload/v1690000000/default-product.png")
    especie = db.Column(db.String(50), nullable=False, default='Geral')

    def to_dict(self):
        return {
            "id": self.id, 
            "nome": self.nome, 
            "preco": f"{self.preco:.2f}", 
            "descricao": self.descricao,
            "estoque": self.estoque,
            "categoria": self.categoria,
            "imagem_url": self.imagem_url,
            "especie": self.especie
        }