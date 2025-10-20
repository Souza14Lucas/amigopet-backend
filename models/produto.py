from config.extensions import db
from sqlalchemy import text

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
    especie = db.Column(db.String(50), nullable=False, default='Geral')

    def to_dict(self):
        return {
            "id": self.id, 
            "nome": self.nome, 
            # Converte Numeric para string para JSON, garantindo 2 casas decimais
            "preco": f"{self.preco:.2f}", 
            "descricao": self.descricao,
            "estoque": self.estoque,
            "categoria": self.categoria,
            "imagem_url": self.imagem_url,
            "especie": self.especie
        }