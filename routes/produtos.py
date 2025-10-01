from flask import Blueprint, jsonify, request
from config.extensions import db 
from utils.security import token_required
from config.models import Produto # <--- Importa o modelo. NÃO o define aqui!
from sqlalchemy.exc import IntegrityError

produtos_bp = Blueprint('produtos', __name__)

# Permite redefinir a tabela se já existir
class Produto(db.Model):
    __tablename__ = "produtos"
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    preco = db.Column(db.Float, nullable=False)
    descricao = db.Column(db.Text)
    categoria = db.Column(db.String(50))
    estoque = db.Column(db.Integer, default=0)
    imagem_url = db.Column(db.String(255), default="https://res.cloudinary.com/demo/image/upload/v1690000000/default-product.png")

    def to_dict(self):
        return {"id": self.id, "nome": self.nome, "preco": self.preco, "descricao": self.descricao, "categoria": self.categoria, "estoque": self.estoque, "imagem_url": self.imagem_url}

# ---------------------------
# Criar produto (apenas admin)
# ---------------------------
@produtos_bp.route('/', methods=['POST'])
@token_required
def create_produto(current_user):
    if current_user['type'] != 'admin':
        return jsonify({"message": "Permissão negada. Apenas administradores podem criar produtos."}), 403

    data = request.get_json()
    nome = data.get('nome')
    descricao = data.get('descricao')
    preco = data.get('preco')
    categoria = data.get('categoria')
    estoque = data.get('estoque', 0)

    if not all([nome, preco]):
        return jsonify({"message": "Campos 'nome' e 'preco' são obrigatórios."}), 400

    try:
        novo_produto = Produto(
            nome=nome,
            descricao=descricao,
            preco=preco,
            categoria=categoria,
            estoque=estoque,
            imagem_url=data.get("imagem_url"),
        )
        db.session.add(novo_produto)
        db.session.commit()

        return jsonify({
            "message": f"Produto '{nome}' criado com sucesso por {current_user['sub']}",
            "produto_id": novo_produto.id
        }), 201

    except Exception as e:
        db.session.rollback()
        print(f"Erro ao criar produto: {e}")
        return jsonify({"message": "Ocorreu um erro ao criar o produto."}), 500


# ---------------------------
# Listar produtos
# ---------------------------
# routes/produtos.py (Função get_produtos - CORREÇÃO DE SERIALIZAÇÃO)
@produtos_bp.route('/', methods=['GET'])
def get_produtos():
    try:
        # Busca os objetos Produto do DB
        produtos_query = Produto.query.filter(Produto.estoque > 0).order_by(Produto.id.asc()).all()
        
        # Serializa os produtos, garantindo que o to_dict() seja chamado em cada objeto
        produtos_data = []
        for p in produtos_query:
            produtos_data.append(p.to_dict()) # <--- CRUCIAL: Serializar usando o método

        return jsonify(produtos_data), 200
    
    except Exception as e:
        print(f"Erro ao listar produtos: {e}")
        return jsonify({"message": "Erro interno ao buscar produtos."}), 500


# ---------------------------
# Consultar produto por ID
# ---------------------------
@produtos_bp.route('/<int:produto_id>', methods=['GET'])
def get_produto(produto_id):
    produto = Produto.query.get(produto_id)
    if not produto:
        return jsonify({"message": "Produto não encontrado"}), 404
    return jsonify(produto.to_dict()), 200


# ---------------------------
# Atualizar produto (apenas admin)
# ---------------------------
@produtos_bp.route('/<int:produto_id>', methods=['PUT'])
@token_required
def update_produto(current_user, produto_id):
    if current_user['type'] != 'admin':
        return jsonify({"message": "Permissão negada. Apenas administradores podem atualizar produtos."}), 403

    produto = Produto.query.get(produto_id)
    if not produto:
        return jsonify({"message": "Produto não encontrado."}), 404

    data = request.get_json()
    produto.nome = data.get('nome', produto.nome)
    produto.preco = data.get('preco', produto.preco)
    produto.imagem_url = data.get('imagem_url', produto.imagem_url)

    db.session.commit()
    return jsonify({"message": "Produto atualizado com sucesso!", "produto": produto.to_dict()}), 200


# ---------------------------
# Deletar produto (apenas admin)
# ---------------------------
@produtos_bp.route('/<int:produto_id>', methods=['DELETE'])
@token_required
def delete_produto(current_user, produto_id):
    if current_user['type'] != 'admin':
        return jsonify({"message": "Permissão negada. Apenas administradores podem deletar produtos."}), 403

    produto = Produto.query.get(produto_id)
    if not produto:
        return jsonify({"message": "Produto não encontrado."}), 404

    db.session.delete(produto)
    db.session.commit()
    return jsonify({"message": f"Produto '{produto.nome}' deletado com sucesso!"}), 200