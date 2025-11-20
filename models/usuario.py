from config.extensions import db
from sqlalchemy import text

class Usuario(db.Model):
    __tablename__ = "usuarios"
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    senha_hash = db.Column(db.Text, nullable=False)
    tipo = db.Column(db.String(20), default='cliente') # 'cliente' ou 'admin'
    created_at = db.Column(db.DateTime, default=text('CURRENT_TIMESTAMP'))
    
    def to_dict(self):
        return {"id": self.id, "email": self.email, "tipo": self.tipo, "nome": self.nome}
